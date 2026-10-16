# Author dependency-inventory precision

The historical develop.py runner records the complete auxiliary dependency
directory before each target compile. Its arrays named dependency_sources
and dependency_objects are a directory inventory, not the exact direct-import
closure. After the successful physical-only Saturation attempt001, that
directory included an older Agent14CarryfreeSaturation source and object.
Consequently later attempt receipts list a stale same-module entry alongside
the actual imported dependency files.

The frozen final attempt004 source has SHA256
2427fcac82b20afe208ae2529b1dc9436217395eef63fcceb707447b0064171a and imports only
Agent14CarryfreeResidues, Agent14CarryfreeDigits and Agent14CarryfreeCoordinates.
It does not import itself. The independent semantic reviewer checked both
the actual source snapshot and the exact registered import map. No old
receipt has been changed to imply a smaller directory inventory or a fresh
source build.

The independent verifier compiled the complete five-source project closure
in a new canonical directory and then again in a separate initially empty
strict-build directory, with no author or canonical object reused for the
strict build. Its module resolution, source hashes and declaration-origin
audits supply the complete acceptance evidence. Refer to the independent
review and raw verification record for exact execution rather than treating
the author's broad inventory as that stronger gate.
