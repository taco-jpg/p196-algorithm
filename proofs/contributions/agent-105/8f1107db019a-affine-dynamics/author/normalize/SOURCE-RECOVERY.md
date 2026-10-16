# Source recovery note

The GitHub connector returned complete UTF-8 file contents with exactly one terminal newline. The initial local restoration included one additional terminal newline for Agent1RepeatedBlock.lean and its registry. Attempts 001–004 compiled the same Lean tokens with this additional trailing whitespace.

The snapshot has now been corrected to the exact fetched bytes, verified against the published Git object identifiers (source 4adf4bd714be87ef5d95f0e6d33632fe36075ca4; registry 3c467def3e9e82190200c7a02c55ae03423ba96c). No Lean token or proof content was changed. The current dependency-pins.json records the corrected source hash. A later compilation will rebuild the corrected Agent1RepeatedBlock module.
