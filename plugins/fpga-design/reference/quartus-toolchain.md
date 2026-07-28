# Quartus toolchain reference

Vendor-specific lookup material for the `fpga-design` skills. This is *reference*,
not process — the skills say what to do, this says how the tool behaves.

Everything here was measured, not recalled. Where a figure appears, it came from a
real run.

## Log codes that mean the build is void

| code | severity | meaning |
|---|---|---|
| `332012` | Critical Warning | SDC file not found; `derive_clocks -period 1.0` used instead |
| `332144` | Info | No user-constrained base clocks found |
| `332142` | Info | Falling back to derived clocks |
| `332130` | Info | Timing requirements not specified; quality may be sacrificed |
| `169085` | Critical Warning | No exact pin location assignments; placement not reproducible |
| `332148` | Critical Warning | Timing requirements not met — meaningless if any of the above fired |

Note that three of these are logged at **Info** severity while describing a condition
that invalidates the build. Severity is not a reliable filter; grep for the codes.

## Log codes worth reading

| code | meaning |
|---|---|
| `19000` | "Inferred N megafunctions from design logic" — the inference summary |
| `276029` | Names each inferred `altsyncram` (block memory) |
| `276020` | Pass-through logic added to match read-during-write behaviour |
| `21061` | Logic cell count after synthesis |
| `21064` | RAM segment count after synthesis |
| `292013` | A feature needs a subscription licence (e.g. LogicLock in Lite) |

## Editions and licensing

| edition | cost | Cyclone V | note |
|---|---|---|---|
| Prime **Lite** | free, no licence file | yes, including `5CEFA9F23I7` | version 19.1 is the last with Cyclone V |
| Prime **Standard** | paid subscription | yes | `Error (292025): License file is not specified` without one |
| Prime **Pro** | paid | **no** | Arria/Stratix/Agilex only; dropped Cyclone V |

Quartus Pro cannot target Cyclone V at all, so a Pro container is not a substitute.

## Containers

Altera and Intel publish official images on Docker Hub:

- `alterafpga/quartusstd-v24.1:cyclonev` — Standard 24.1, 6 GB compressed / 12.4 GB on
  disk. Needs a licence.
- `alterafpga/quartuspro-*`, `intel/quartuspro-*` — Pro, ~20 GB, no Cyclone V.
- There is **no official Lite image**; community images exist for it.

## Running Quartus on Apple Silicon

Three obstacles, in the order you hit them.

### 1. Rosetta cannot run current Quartus

Quartus 24.1 Standard dies immediately under Rosetta — every `quartus_*` binary:

```
*** Fatal Error: Illegal Instruction
Module: quartus_sh
Stack Trace:
    0x1af7f: hasHighPrecisionDouble + 0x42 (ccl_sqlite3)
```

Quartus **19.1 Lite** does run under Rosetta. Older binaries use a narrower instruction
set. Prefer it.

### 2. Under QEMU, Quartus refuses to start

If you force QEMU (disable the `rosetta` binfmt handler), Quartus 24.1 gets past the
illegal instruction but then reports:

```
The Quartus II software is optimized for the Intel Pentium III processor
and newer processors.  The required extensions were not found on: ''
```

Because QEMU-user exposes the **arm64** host's `/proc/cpuinfo`, so Quartus finds no SSE.
Bind-mounting a synthetic x86 `cpuinfo` over `/proc/cpuinfo` gets it running — but
`quartus_fit` then segfaults, so this is a dead end for a full flow.

Both binfmt handlers can be registered at once; check which is active by looking for
`/run/rosetta` in `/proc/self/maps` **inside the process** (looking for the file in the
container filesystem proves nothing — the handler lives in the VM).

### 3. Without `--init`, the fitter deadlocks

`quartus_map` running as PID 1 never reaps its forked workers:

```
PID  STAT  ELAPSED  COMMAND
  1  Ssl     30:45  quartus_map        <- sleeping in wait_for_partner
179  Z       30:01  quartus_map <defunct>
180  Z       30:01  quartus_map <defunct>
181  Z       30:01  quartus_map <defunct>
```

Observed hanging 30 minutes at 4% CPU. Two fixes, apply both:

- `docker run --init` so a real init reaps children.
- `set_global_assignment -name NUM_PARALLEL_PROCESSORS 1` to avoid the fork entirely.

### A working wrapper

```sh
#!/bin/sh
set -e
DIR=$(cd "$1" && pwd); shift
exec docker run --rm --init --platform linux/amd64 \
  -v "$DIR:/work" -w /work -e HOME=/work \
  -e PATH=/opt/intelFPGA_lite/quartus/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin \
  <quartus-lite-19.1-image> bash -c "$*"
```

## Measured runtimes

PicoRV32 SoC (RV32I core, 8 KB RAM, GPIO) on `5CEFA9F23I7`, under Rosetta on an
M3 Max:

| stage | time |
|---|---|
| `quartus_map` | 20 s |
| `quartus_fit` | 1 min 8 s |
| `quartus_asm` | 9 s |
| `quartus_sta` | 10 s |

Emulation is not the bottleneck people expect; a full flow on a small design is about
two minutes.

## Output file locations

`quartus_asm` writes `<rev>.sof` into the **project root**, not `output_files/`, unless
the QSF says otherwise. `quartus_cpf -c top.sof top.rbf` converts to a raw bitstream.
