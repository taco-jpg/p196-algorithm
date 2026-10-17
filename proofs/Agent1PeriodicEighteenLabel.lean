import Agent1PeriodicOuterRank

/-!
The preserved total component-label definition assigns label130 only to
the constant-eighteen phase. The proof follows its existing constructor
and digit decisions directly; no graph rows or catalog premise are used.
-/

set_option maxHeartbeats 1600000

namespace Agent1.Periodic

theorem outerComponent_eighteen_phase (s : OuterNode)
    (hc : outerComponent s = 130) : s.1 = [18,18,18,18] := by
  rcases s with ⟨w, a⟩
  delta outerComponent outerComponent.match_9 at hc
  cases w with
  | nil =>
      dsimp only at hc
      contradiction
  | cons x0 tail0 =>
      dsimp only at hc
      by_cases h0_0 : x0 = 0
      · rw [dif_pos h0_0] at hc
        subst x0
        dsimp only at hc
        cases tail0 with
        | nil =>
            dsimp only at hc
            contradiction
        | cons x1 tail1 =>
            dsimp only at hc
            by_cases h1_0 : x1 = 0
            · rw [dif_pos h1_0] at hc
              subst x1
              dsimp only at hc
              cases tail1 with
              | nil =>
                  dsimp only at hc
                  contradiction
              | cons x2 tail2 =>
                  dsimp only at hc
                  by_cases h2_0 : x2 = 0
                  · rw [dif_pos h2_0] at hc
                    subst x2
                    dsimp only at hc
                    cases tail2 with
                    | nil =>
                        dsimp only at hc
                        contradiction
                    | cons x3 tail3 =>
                        dsimp only at hc
                        by_cases h3_0 : x3 = 0
                        · rw [dif_pos h3_0] at hc
                          subst x3
                          dsimp only at hc
                          cases tail3 with
                          | nil =>
                              dsimp only at hc
                              contradiction
                          | cons _ _ =>
                              dsimp only at hc
                              contradiction
                        · rw [dif_neg h3_0] at hc
                          contradiction
                  · rw [dif_neg h2_0] at hc
                    contradiction
            · rw [dif_neg h1_0] at hc
              contradiction
      · rw [dif_neg h0_0] at hc
        by_cases h0_9 : x0 = 9
        · rw [dif_pos h0_9] at hc
          subst x0
          dsimp only at hc
          cases tail0 with
          | nil =>
              dsimp only at hc
              contradiction
          | cons x1 tail1 =>
              dsimp only at hc
              by_cases h1_9 : x1 = 9
              · rw [dif_pos h1_9] at hc
                subst x1
                dsimp only at hc
                cases tail1 with
                | nil =>
                    dsimp only at hc
                    contradiction
                | cons x2 tail2 =>
                    dsimp only at hc
                    by_cases h2_9 : x2 = 9
                    · rw [dif_pos h2_9] at hc
                      subst x2
                      dsimp only at hc
                      cases tail2 with
                      | nil =>
                          dsimp only at hc
                          contradiction
                      | cons x3 tail3 =>
                          dsimp only at hc
                          by_cases h3_9 : x3 = 9
                          · rw [dif_pos h3_9] at hc
                            subst x3
                            dsimp only at hc
                            cases tail3 with
                            | nil =>
                                dsimp only at hc
                                contradiction
                            | cons _ _ =>
                                dsimp only at hc
                                contradiction
                          · rw [dif_neg h3_9] at hc
                            contradiction
                    · rw [dif_neg h2_9] at hc
                      contradiction
              · rw [dif_neg h1_9] at hc
                by_cases h1_2 : x1 = 2
                · rw [dif_pos h1_2] at hc
                  subst x1
                  dsimp only at hc
                  cases tail1 with
                  | nil =>
                      dsimp only at hc
                      contradiction
                  | cons x2 tail2 =>
                      dsimp only at hc
                      by_cases h2_9 : x2 = 9
                      · rw [dif_pos h2_9] at hc
                        subst x2
                        dsimp only at hc
                        cases tail2 with
                        | nil =>
                            dsimp only at hc
                            contradiction
                        | cons x3 tail3 =>
                            dsimp only at hc
                            by_cases h3_16 : x3 = 16
                            · rw [dif_pos h3_16] at hc
                              subst x3
                              dsimp only at hc
                              cases tail3 with
                              | nil =>
                                  dsimp only at hc
                                  split at hc <;> contradiction
                              | cons _ _ =>
                                  dsimp only at hc
                                  contradiction
                            · rw [dif_neg h3_16] at hc
                              contradiction
                      · rw [dif_neg h2_9] at hc
                        contradiction
                · rw [dif_neg h1_2] at hc
                  by_cases h1_4 : x1 = 4
                  · rw [dif_pos h1_4] at hc
                    subst x1
                    dsimp only at hc
                    cases tail1 with
                    | nil =>
                        dsimp only at hc
                        contradiction
                    | cons x2 tail2 =>
                        dsimp only at hc
                        by_cases h2_9 : x2 = 9
                        · rw [dif_pos h2_9] at hc
                          subst x2
                          dsimp only at hc
                          cases tail2 with
                          | nil =>
                              dsimp only at hc
                              contradiction
                          | cons x3 tail3 =>
                              dsimp only at hc
                              by_cases h3_14 : x3 = 14
                              · rw [dif_pos h3_14] at hc
                                subst x3
                                dsimp only at hc
                                cases tail3 with
                                | nil =>
                                    dsimp only at hc
                                    split at hc <;> contradiction
                                | cons _ _ =>
                                    dsimp only at hc
                                    contradiction
                              · rw [dif_neg h3_14] at hc
                                contradiction
                        · rw [dif_neg h2_9] at hc
                          contradiction
                  · rw [dif_neg h1_4] at hc
                    by_cases h1_6 : x1 = 6
                    · rw [dif_pos h1_6] at hc
                      subst x1
                      dsimp only at hc
                      cases tail1 with
                      | nil =>
                          dsimp only at hc
                          contradiction
                      | cons x2 tail2 =>
                          dsimp only at hc
                          by_cases h2_9 : x2 = 9
                          · rw [dif_pos h2_9] at hc
                            subst x2
                            dsimp only at hc
                            cases tail2 with
                            | nil =>
                                dsimp only at hc
                                contradiction
                            | cons x3 tail3 =>
                                dsimp only at hc
                                by_cases h3_12 : x3 = 12
                                · rw [dif_pos h3_12] at hc
                                  subst x3
                                  dsimp only at hc
                                  cases tail3 with
                                  | nil =>
                                      dsimp only at hc
                                      split at hc <;> contradiction
                                  | cons _ _ =>
                                      dsimp only at hc
                                      contradiction
                                · rw [dif_neg h3_12] at hc
                                  contradiction
                          · rw [dif_neg h2_9] at hc
                            contradiction
                    · rw [dif_neg h1_6] at hc
                      by_cases h1_12 : x1 = 12
                      · rw [dif_pos h1_12] at hc
                        subst x1
                        dsimp only at hc
                        cases tail1 with
                        | nil =>
                            dsimp only at hc
                            contradiction
                        | cons x2 tail2 =>
                            dsimp only at hc
                            by_cases h2_9 : x2 = 9
                            · rw [dif_pos h2_9] at hc
                              subst x2
                              dsimp only at hc
                              cases tail2 with
                              | nil =>
                                  dsimp only at hc
                                  contradiction
                              | cons x3 tail3 =>
                                  dsimp only at hc
                                  by_cases h3_6 : x3 = 6
                                  · rw [dif_pos h3_6] at hc
                                    subst x3
                                    dsimp only at hc
                                    cases tail3 with
                                    | nil =>
                                        dsimp only at hc
                                        split at hc <;> contradiction
                                    | cons _ _ =>
                                        dsimp only at hc
                                        contradiction
                                  · rw [dif_neg h3_6] at hc
                                    contradiction
                            · rw [dif_neg h2_9] at hc
                              contradiction
                      · rw [dif_neg h1_12] at hc
                        by_cases h1_14 : x1 = 14
                        · rw [dif_pos h1_14] at hc
                          subst x1
                          dsimp only at hc
                          cases tail1 with
                          | nil =>
                              dsimp only at hc
                              contradiction
                          | cons x2 tail2 =>
                              dsimp only at hc
                              by_cases h2_9 : x2 = 9
                              · rw [dif_pos h2_9] at hc
                                subst x2
                                dsimp only at hc
                                cases tail2 with
                                | nil =>
                                    dsimp only at hc
                                    contradiction
                                | cons x3 tail3 =>
                                    dsimp only at hc
                                    by_cases h3_4 : x3 = 4
                                    · rw [dif_pos h3_4] at hc
                                      subst x3
                                      dsimp only at hc
                                      cases tail3 with
                                      | nil =>
                                          dsimp only at hc
                                          split at hc <;> contradiction
                                      | cons _ _ =>
                                          dsimp only at hc
                                          contradiction
                                    · rw [dif_neg h3_4] at hc
                                      contradiction
                              · rw [dif_neg h2_9] at hc
                                contradiction
                        · rw [dif_neg h1_14] at hc
                          by_cases h1_16 : x1 = 16
                          · rw [dif_pos h1_16] at hc
                            subst x1
                            dsimp only at hc
                            cases tail1 with
                            | nil =>
                                dsimp only at hc
                                contradiction
                            | cons x2 tail2 =>
                                dsimp only at hc
                                by_cases h2_9 : x2 = 9
                                · rw [dif_pos h2_9] at hc
                                  subst x2
                                  dsimp only at hc
                                  cases tail2 with
                                  | nil =>
                                      dsimp only at hc
                                      contradiction
                                  | cons x3 tail3 =>
                                      dsimp only at hc
                                      by_cases h3_2 : x3 = 2
                                      · rw [dif_pos h3_2] at hc
                                        subst x3
                                        dsimp only at hc
                                        cases tail3 with
                                        | nil =>
                                            dsimp only at hc
                                            split at hc <;> contradiction
                                        | cons _ _ =>
                                            dsimp only at hc
                                            contradiction
                                      · rw [dif_neg h3_2] at hc
                                        contradiction
                                · rw [dif_neg h2_9] at hc
                                  contradiction
                          · rw [dif_neg h1_16] at hc
                            contradiction
        · rw [dif_neg h0_9] at hc
          by_cases h0_18 : x0 = 18
          · rw [dif_pos h0_18] at hc
            subst x0
            dsimp only at hc
            cases tail0 with
            | nil =>
                dsimp only at hc
                contradiction
            | cons x1 tail1 =>
                dsimp only at hc
                by_cases h1_18 : x1 = 18
                · rw [dif_pos h1_18] at hc
                  subst x1
                  dsimp only at hc
                  cases tail1 with
                  | nil =>
                      dsimp only at hc
                      contradiction
                  | cons x2 tail2 =>
                      dsimp only at hc
                      by_cases h2_18 : x2 = 18
                      · rw [dif_pos h2_18] at hc
                        subst x2
                        dsimp only at hc
                        cases tail2 with
                        | nil =>
                            dsimp only at hc
                            contradiction
                        | cons x3 tail3 =>
                            dsimp only at hc
                            by_cases h3_18 : x3 = 18
                            · rw [dif_pos h3_18] at hc
                              subst x3
                              dsimp only at hc
                              cases tail3 with
                              | nil =>
                                  dsimp only at hc
                                  rfl
                              | cons _ _ =>
                                  dsimp only at hc
                                  contradiction
                            · rw [dif_neg h3_18] at hc
                              contradiction
                      · rw [dif_neg h2_18] at hc
                        contradiction
                · rw [dif_neg h1_18] at hc
                  contradiction
          · rw [dif_neg h0_18] at hc
            by_cases h0_1 : x0 = 1
            · rw [dif_pos h0_1] at hc
              subst x0
              dsimp only at hc
              cases tail0 with
              | nil =>
                  dsimp only at hc
                  contradiction
              | cons x1 tail1 =>
                  dsimp only at hc
                  by_cases h1_1 : x1 = 1
                  · rw [dif_pos h1_1] at hc
                    subst x1
                    dsimp only at hc
                    cases tail1 with
                    | nil =>
                        dsimp only at hc
                        contradiction
                    | cons x2 tail2 =>
                        dsimp only at hc
                        by_cases h2_17 : x2 = 17
                        · rw [dif_pos h2_17] at hc
                          subst x2
                          dsimp only at hc
                          cases tail2 with
                          | nil =>
                              dsimp only at hc
                              contradiction
                          | cons x3 tail3 =>
                              dsimp only at hc
                              by_cases h3_17 : x3 = 17
                              · rw [dif_pos h3_17] at hc
                                subst x3
                                dsimp only at hc
                                cases tail3 with
                                | nil =>
                                    dsimp only at hc
                                    split at hc <;> contradiction
                                | cons _ _ =>
                                    dsimp only at hc
                                    contradiction
                              · rw [dif_neg h3_17] at hc
                                contradiction
                        · rw [dif_neg h2_17] at hc
                          contradiction
                  · rw [dif_neg h1_1] at hc
                    by_cases h1_17 : x1 = 17
                    · rw [dif_pos h1_17] at hc
                      subst x1
                      dsimp only at hc
                      cases tail1 with
                      | nil =>
                          dsimp only at hc
                          contradiction
                      | cons x2 tail2 =>
                          dsimp only at hc
                          by_cases h2_17 : x2 = 17
                          · rw [dif_pos h2_17] at hc
                            subst x2
                            dsimp only at hc
                            cases tail2 with
                            | nil =>
                                dsimp only at hc
                                contradiction
                            | cons x3 tail3 =>
                                dsimp only at hc
                                by_cases h3_1 : x3 = 1
                                · rw [dif_pos h3_1] at hc
                                  subst x3
                                  dsimp only at hc
                                  cases tail3 with
                                  | nil =>
                                      dsimp only at hc
                                      split at hc <;> contradiction
                                  | cons _ _ =>
                                      dsimp only at hc
                                      contradiction
                                · rw [dif_neg h3_1] at hc
                                  contradiction
                          · rw [dif_neg h2_17] at hc
                            contradiction
                    · rw [dif_neg h1_17] at hc
                      contradiction
            · rw [dif_neg h0_1] at hc
              by_cases h0_2 : x0 = 2
              · rw [dif_pos h0_2] at hc
                subst x0
                dsimp only at hc
                cases tail0 with
                | nil =>
                    dsimp only at hc
                    contradiction
                | cons x1 tail1 =>
                    dsimp only at hc
                    by_cases h1_9 : x1 = 9
                    · rw [dif_pos h1_9] at hc
                      subst x1
                      dsimp only at hc
                      cases tail1 with
                      | nil =>
                          dsimp only at hc
                          contradiction
                      | cons x2 tail2 =>
                          dsimp only at hc
                          by_cases h2_16 : x2 = 16
                          · rw [dif_pos h2_16] at hc
                            subst x2
                            dsimp only at hc
                            cases tail2 with
                            | nil =>
                                dsimp only at hc
                                contradiction
                            | cons x3 tail3 =>
                                dsimp only at hc
                                by_cases h3_9 : x3 = 9
                                · rw [dif_pos h3_9] at hc
                                  subst x3
                                  dsimp only at hc
                                  cases tail3 with
                                  | nil =>
                                      dsimp only at hc
                                      split at hc <;> contradiction
                                  | cons _ _ =>
                                      dsimp only at hc
                                      contradiction
                                · rw [dif_neg h3_9] at hc
                                  contradiction
                          · rw [dif_neg h2_16] at hc
                            contradiction
                    · rw [dif_neg h1_9] at hc
                      contradiction
              · rw [dif_neg h0_2] at hc
                by_cases h0_3 : x0 = 3
                · rw [dif_pos h0_3] at hc
                  subst x0
                  dsimp only at hc
                  cases tail0 with
                  | nil =>
                      dsimp only at hc
                      contradiction
                  | cons x1 tail1 =>
                      dsimp only at hc
                      by_cases h1_3 : x1 = 3
                      · rw [dif_pos h1_3] at hc
                        subst x1
                        dsimp only at hc
                        cases tail1 with
                        | nil =>
                            dsimp only at hc
                            contradiction
                        | cons x2 tail2 =>
                            dsimp only at hc
                            by_cases h2_15 : x2 = 15
                            · rw [dif_pos h2_15] at hc
                              subst x2
                              dsimp only at hc
                              cases tail2 with
                              | nil =>
                                  dsimp only at hc
                                  contradiction
                              | cons x3 tail3 =>
                                  dsimp only at hc
                                  by_cases h3_15 : x3 = 15
                                  · rw [dif_pos h3_15] at hc
                                    subst x3
                                    dsimp only at hc
                                    cases tail3 with
                                    | nil =>
                                        dsimp only at hc
                                        split at hc <;> contradiction
                                    | cons _ _ =>
                                        dsimp only at hc
                                        contradiction
                                  · rw [dif_neg h3_15] at hc
                                    contradiction
                            · rw [dif_neg h2_15] at hc
                              contradiction
                      · rw [dif_neg h1_3] at hc
                        by_cases h1_15 : x1 = 15
                        · rw [dif_pos h1_15] at hc
                          subst x1
                          dsimp only at hc
                          cases tail1 with
                          | nil =>
                              dsimp only at hc
                              contradiction
                          | cons x2 tail2 =>
                              dsimp only at hc
                              by_cases h2_15 : x2 = 15
                              · rw [dif_pos h2_15] at hc
                                subst x2
                                dsimp only at hc
                                cases tail2 with
                                | nil =>
                                    dsimp only at hc
                                    contradiction
                                | cons x3 tail3 =>
                                    dsimp only at hc
                                    by_cases h3_3 : x3 = 3
                                    · rw [dif_pos h3_3] at hc
                                      subst x3
                                      dsimp only at hc
                                      cases tail3 with
                                      | nil =>
                                          dsimp only at hc
                                          split at hc <;> contradiction
                                      | cons _ _ =>
                                          dsimp only at hc
                                          contradiction
                                    · rw [dif_neg h3_3] at hc
                                      contradiction
                              · rw [dif_neg h2_15] at hc
                                contradiction
                        · rw [dif_neg h1_15] at hc
                          contradiction
                · rw [dif_neg h0_3] at hc
                  by_cases h0_4 : x0 = 4
                  · rw [dif_pos h0_4] at hc
                    subst x0
                    dsimp only at hc
                    cases tail0 with
                    | nil =>
                        dsimp only at hc
                        contradiction
                    | cons x1 tail1 =>
                        dsimp only at hc
                        by_cases h1_4 : x1 = 4
                        · rw [dif_pos h1_4] at hc
                          subst x1
                          dsimp only at hc
                          cases tail1 with
                          | nil =>
                              dsimp only at hc
                              contradiction
                          | cons x2 tail2 =>
                              dsimp only at hc
                              by_cases h2_14 : x2 = 14
                              · rw [dif_pos h2_14] at hc
                                subst x2
                                dsimp only at hc
                                cases tail2 with
                                | nil =>
                                    dsimp only at hc
                                    contradiction
                                | cons x3 tail3 =>
                                    dsimp only at hc
                                    by_cases h3_14 : x3 = 14
                                    · rw [dif_pos h3_14] at hc
                                      subst x3
                                      dsimp only at hc
                                      cases tail3 with
                                      | nil =>
                                          dsimp only at hc
                                          split at hc <;> contradiction
                                      | cons _ _ =>
                                          dsimp only at hc
                                          contradiction
                                    · rw [dif_neg h3_14] at hc
                                      contradiction
                              · rw [dif_neg h2_14] at hc
                                contradiction
                        · rw [dif_neg h1_4] at hc
                          by_cases h1_9 : x1 = 9
                          · rw [dif_pos h1_9] at hc
                            subst x1
                            dsimp only at hc
                            cases tail1 with
                            | nil =>
                                dsimp only at hc
                                contradiction
                            | cons x2 tail2 =>
                                dsimp only at hc
                                by_cases h2_14 : x2 = 14
                                · rw [dif_pos h2_14] at hc
                                  subst x2
                                  dsimp only at hc
                                  cases tail2 with
                                  | nil =>
                                      dsimp only at hc
                                      contradiction
                                  | cons x3 tail3 =>
                                      dsimp only at hc
                                      by_cases h3_9 : x3 = 9
                                      · rw [dif_pos h3_9] at hc
                                        subst x3
                                        dsimp only at hc
                                        cases tail3 with
                                        | nil =>
                                            dsimp only at hc
                                            split at hc <;> contradiction
                                        | cons _ _ =>
                                            dsimp only at hc
                                            contradiction
                                      · rw [dif_neg h3_9] at hc
                                        contradiction
                                · rw [dif_neg h2_14] at hc
                                  contradiction
                          · rw [dif_neg h1_9] at hc
                            by_cases h1_14 : x1 = 14
                            · rw [dif_pos h1_14] at hc
                              subst x1
                              dsimp only at hc
                              cases tail1 with
                              | nil =>
                                  dsimp only at hc
                                  contradiction
                              | cons x2 tail2 =>
                                  dsimp only at hc
                                  by_cases h2_14 : x2 = 14
                                  · rw [dif_pos h2_14] at hc
                                    subst x2
                                    dsimp only at hc
                                    cases tail2 with
                                    | nil =>
                                        dsimp only at hc
                                        contradiction
                                    | cons x3 tail3 =>
                                        dsimp only at hc
                                        by_cases h3_4 : x3 = 4
                                        · rw [dif_pos h3_4] at hc
                                          subst x3
                                          dsimp only at hc
                                          cases tail3 with
                                          | nil =>
                                              dsimp only at hc
                                              split at hc <;> contradiction
                                          | cons _ _ =>
                                              dsimp only at hc
                                              contradiction
                                        · rw [dif_neg h3_4] at hc
                                          contradiction
                                  · rw [dif_neg h2_14] at hc
                                    contradiction
                            · rw [dif_neg h1_14] at hc
                              contradiction
                  · rw [dif_neg h0_4] at hc
                    by_cases h0_6 : x0 = 6
                    · rw [dif_pos h0_6] at hc
                      subst x0
                      dsimp only at hc
                      cases tail0 with
                      | nil =>
                          dsimp only at hc
                          contradiction
                      | cons x1 tail1 =>
                          dsimp only at hc
                          by_cases h1_9 : x1 = 9
                          · rw [dif_pos h1_9] at hc
                            subst x1
                            dsimp only at hc
                            cases tail1 with
                            | nil =>
                                dsimp only at hc
                                contradiction
                            | cons x2 tail2 =>
                                dsimp only at hc
                                by_cases h2_12 : x2 = 12
                                · rw [dif_pos h2_12] at hc
                                  subst x2
                                  dsimp only at hc
                                  cases tail2 with
                                  | nil =>
                                      dsimp only at hc
                                      contradiction
                                  | cons x3 tail3 =>
                                      dsimp only at hc
                                      by_cases h3_9 : x3 = 9
                                      · rw [dif_pos h3_9] at hc
                                        subst x3
                                        dsimp only at hc
                                        cases tail3 with
                                        | nil =>
                                            dsimp only at hc
                                            split at hc <;> contradiction
                                        | cons _ _ =>
                                            dsimp only at hc
                                            contradiction
                                      · rw [dif_neg h3_9] at hc
                                        contradiction
                                · rw [dif_neg h2_12] at hc
                                  contradiction
                          · rw [dif_neg h1_9] at hc
                            contradiction
                    · rw [dif_neg h0_6] at hc
                      by_cases h0_7 : x0 = 7
                      · rw [dif_pos h0_7] at hc
                        subst x0
                        dsimp only at hc
                        cases tail0 with
                        | nil =>
                            dsimp only at hc
                            contradiction
                        | cons x1 tail1 =>
                            dsimp only at hc
                            by_cases h1_7 : x1 = 7
                            · rw [dif_pos h1_7] at hc
                              subst x1
                              dsimp only at hc
                              cases tail1 with
                              | nil =>
                                  dsimp only at hc
                                  contradiction
                              | cons x2 tail2 =>
                                  dsimp only at hc
                                  by_cases h2_11 : x2 = 11
                                  · rw [dif_pos h2_11] at hc
                                    subst x2
                                    dsimp only at hc
                                    cases tail2 with
                                    | nil =>
                                        dsimp only at hc
                                        contradiction
                                    | cons x3 tail3 =>
                                        dsimp only at hc
                                        by_cases h3_11 : x3 = 11
                                        · rw [dif_pos h3_11] at hc
                                          subst x3
                                          dsimp only at hc
                                          cases tail3 with
                                          | nil =>
                                              dsimp only at hc
                                              split at hc <;> contradiction
                                          | cons _ _ =>
                                              dsimp only at hc
                                              contradiction
                                        · rw [dif_neg h3_11] at hc
                                          contradiction
                                  · rw [dif_neg h2_11] at hc
                                    contradiction
                            · rw [dif_neg h1_7] at hc
                              by_cases h1_11 : x1 = 11
                              · rw [dif_pos h1_11] at hc
                                subst x1
                                dsimp only at hc
                                cases tail1 with
                                | nil =>
                                    dsimp only at hc
                                    contradiction
                                | cons x2 tail2 =>
                                    dsimp only at hc
                                    by_cases h2_11 : x2 = 11
                                    · rw [dif_pos h2_11] at hc
                                      subst x2
                                      dsimp only at hc
                                      cases tail2 with
                                      | nil =>
                                          dsimp only at hc
                                          contradiction
                                      | cons x3 tail3 =>
                                          dsimp only at hc
                                          by_cases h3_7 : x3 = 7
                                          · rw [dif_pos h3_7] at hc
                                            subst x3
                                            dsimp only at hc
                                            cases tail3 with
                                            | nil =>
                                                dsimp only at hc
                                                split at hc <;> contradiction
                                            | cons _ _ =>
                                                dsimp only at hc
                                                contradiction
                                          · rw [dif_neg h3_7] at hc
                                            contradiction
                                    · rw [dif_neg h2_11] at hc
                                      contradiction
                              · rw [dif_neg h1_11] at hc
                                contradiction
                      · rw [dif_neg h0_7] at hc
                        by_cases h0_11 : x0 = 11
                        · rw [dif_pos h0_11] at hc
                          subst x0
                          dsimp only at hc
                          cases tail0 with
                          | nil =>
                              dsimp only at hc
                              contradiction
                          | cons x1 tail1 =>
                              dsimp only at hc
                              by_cases h1_7 : x1 = 7
                              · rw [dif_pos h1_7] at hc
                                subst x1
                                dsimp only at hc
                                cases tail1 with
                                | nil =>
                                    dsimp only at hc
                                    contradiction
                                | cons x2 tail2 =>
                                    dsimp only at hc
                                    by_cases h2_7 : x2 = 7
                                    · rw [dif_pos h2_7] at hc
                                      subst x2
                                      dsimp only at hc
                                      cases tail2 with
                                      | nil =>
                                          dsimp only at hc
                                          contradiction
                                      | cons x3 tail3 =>
                                          dsimp only at hc
                                          by_cases h3_11 : x3 = 11
                                          · rw [dif_pos h3_11] at hc
                                            subst x3
                                            dsimp only at hc
                                            cases tail3 with
                                            | nil =>
                                                dsimp only at hc
                                                split at hc <;> contradiction
                                            | cons _ _ =>
                                                dsimp only at hc
                                                contradiction
                                          · rw [dif_neg h3_11] at hc
                                            contradiction
                                    · rw [dif_neg h2_7] at hc
                                      contradiction
                              · rw [dif_neg h1_7] at hc
                                by_cases h1_11 : x1 = 11
                                · rw [dif_pos h1_11] at hc
                                  subst x1
                                  dsimp only at hc
                                  cases tail1 with
                                  | nil =>
                                      dsimp only at hc
                                      contradiction
                                  | cons x2 tail2 =>
                                      dsimp only at hc
                                      by_cases h2_7 : x2 = 7
                                      · rw [dif_pos h2_7] at hc
                                        subst x2
                                        dsimp only at hc
                                        cases tail2 with
                                        | nil =>
                                            dsimp only at hc
                                            contradiction
                                        | cons x3 tail3 =>
                                            dsimp only at hc
                                            by_cases h3_7 : x3 = 7
                                            · rw [dif_pos h3_7] at hc
                                              subst x3
                                              dsimp only at hc
                                              cases tail3 with
                                              | nil =>
                                                  dsimp only at hc
                                                  split at hc <;> contradiction
                                              | cons _ _ =>
                                                  dsimp only at hc
                                                  contradiction
                                            · rw [dif_neg h3_7] at hc
                                              contradiction
                                      · rw [dif_neg h2_7] at hc
                                        contradiction
                                · rw [dif_neg h1_11] at hc
                                  contradiction
                        · rw [dif_neg h0_11] at hc
                          by_cases h0_12 : x0 = 12
                          · rw [dif_pos h0_12] at hc
                            subst x0
                            dsimp only at hc
                            cases tail0 with
                            | nil =>
                                dsimp only at hc
                                contradiction
                            | cons x1 tail1 =>
                                dsimp only at hc
                                by_cases h1_9 : x1 = 9
                                · rw [dif_pos h1_9] at hc
                                  subst x1
                                  dsimp only at hc
                                  cases tail1 with
                                  | nil =>
                                      dsimp only at hc
                                      contradiction
                                  | cons x2 tail2 =>
                                      dsimp only at hc
                                      by_cases h2_6 : x2 = 6
                                      · rw [dif_pos h2_6] at hc
                                        subst x2
                                        dsimp only at hc
                                        cases tail2 with
                                        | nil =>
                                            dsimp only at hc
                                            contradiction
                                        | cons x3 tail3 =>
                                            dsimp only at hc
                                            by_cases h3_9 : x3 = 9
                                            · rw [dif_pos h3_9] at hc
                                              subst x3
                                              dsimp only at hc
                                              cases tail3 with
                                              | nil =>
                                                  dsimp only at hc
                                                  split at hc <;> contradiction
                                              | cons _ _ =>
                                                  dsimp only at hc
                                                  contradiction
                                            · rw [dif_neg h3_9] at hc
                                              contradiction
                                      · rw [dif_neg h2_6] at hc
                                        contradiction
                                · rw [dif_neg h1_9] at hc
                                  contradiction
                          · rw [dif_neg h0_12] at hc
                            by_cases h0_14 : x0 = 14
                            · rw [dif_pos h0_14] at hc
                              subst x0
                              dsimp only at hc
                              cases tail0 with
                              | nil =>
                                  dsimp only at hc
                                  contradiction
                              | cons x1 tail1 =>
                                  dsimp only at hc
                                  by_cases h1_4 : x1 = 4
                                  · rw [dif_pos h1_4] at hc
                                    subst x1
                                    dsimp only at hc
                                    cases tail1 with
                                    | nil =>
                                        dsimp only at hc
                                        contradiction
                                    | cons x2 tail2 =>
                                        dsimp only at hc
                                        by_cases h2_4 : x2 = 4
                                        · rw [dif_pos h2_4] at hc
                                          subst x2
                                          dsimp only at hc
                                          cases tail2 with
                                          | nil =>
                                              dsimp only at hc
                                              contradiction
                                          | cons x3 tail3 =>
                                              dsimp only at hc
                                              by_cases h3_14 : x3 = 14
                                              · rw [dif_pos h3_14] at hc
                                                subst x3
                                                dsimp only at hc
                                                cases tail3 with
                                                | nil =>
                                                    dsimp only at hc
                                                    split at hc <;> contradiction
                                                | cons _ _ =>
                                                    dsimp only at hc
                                                    contradiction
                                              · rw [dif_neg h3_14] at hc
                                                contradiction
                                        · rw [dif_neg h2_4] at hc
                                          contradiction
                                  · rw [dif_neg h1_4] at hc
                                    by_cases h1_9 : x1 = 9
                                    · rw [dif_pos h1_9] at hc
                                      subst x1
                                      dsimp only at hc
                                      cases tail1 with
                                      | nil =>
                                          dsimp only at hc
                                          contradiction
                                      | cons x2 tail2 =>
                                          dsimp only at hc
                                          by_cases h2_4 : x2 = 4
                                          · rw [dif_pos h2_4] at hc
                                            subst x2
                                            dsimp only at hc
                                            cases tail2 with
                                            | nil =>
                                                dsimp only at hc
                                                contradiction
                                            | cons x3 tail3 =>
                                                dsimp only at hc
                                                by_cases h3_9 : x3 = 9
                                                · rw [dif_pos h3_9] at hc
                                                  subst x3
                                                  dsimp only at hc
                                                  cases tail3 with
                                                  | nil =>
                                                      dsimp only at hc
                                                      split at hc <;> contradiction
                                                  | cons _ _ =>
                                                      dsimp only at hc
                                                      contradiction
                                                · rw [dif_neg h3_9] at hc
                                                  contradiction
                                          · rw [dif_neg h2_4] at hc
                                            contradiction
                                    · rw [dif_neg h1_9] at hc
                                      by_cases h1_14 : x1 = 14
                                      · rw [dif_pos h1_14] at hc
                                        subst x1
                                        dsimp only at hc
                                        cases tail1 with
                                        | nil =>
                                            dsimp only at hc
                                            contradiction
                                        | cons x2 tail2 =>
                                            dsimp only at hc
                                            by_cases h2_4 : x2 = 4
                                            · rw [dif_pos h2_4] at hc
                                              subst x2
                                              dsimp only at hc
                                              cases tail2 with
                                              | nil =>
                                                  dsimp only at hc
                                                  contradiction
                                              | cons x3 tail3 =>
                                                  dsimp only at hc
                                                  by_cases h3_4 : x3 = 4
                                                  · rw [dif_pos h3_4] at hc
                                                    subst x3
                                                    dsimp only at hc
                                                    cases tail3 with
                                                    | nil =>
                                                        dsimp only at hc
                                                        split at hc <;> contradiction
                                                    | cons _ _ =>
                                                        dsimp only at hc
                                                        contradiction
                                                  · rw [dif_neg h3_4] at hc
                                                    contradiction
                                            · rw [dif_neg h2_4] at hc
                                              contradiction
                                      · rw [dif_neg h1_14] at hc
                                        contradiction
                            · rw [dif_neg h0_14] at hc
                              by_cases h0_15 : x0 = 15
                              · rw [dif_pos h0_15] at hc
                                subst x0
                                dsimp only at hc
                                cases tail0 with
                                | nil =>
                                    dsimp only at hc
                                    contradiction
                                | cons x1 tail1 =>
                                    dsimp only at hc
                                    by_cases h1_3 : x1 = 3
                                    · rw [dif_pos h1_3] at hc
                                      subst x1
                                      dsimp only at hc
                                      cases tail1 with
                                      | nil =>
                                          dsimp only at hc
                                          contradiction
                                      | cons x2 tail2 =>
                                          dsimp only at hc
                                          by_cases h2_3 : x2 = 3
                                          · rw [dif_pos h2_3] at hc
                                            subst x2
                                            dsimp only at hc
                                            cases tail2 with
                                            | nil =>
                                                dsimp only at hc
                                                contradiction
                                            | cons x3 tail3 =>
                                                dsimp only at hc
                                                by_cases h3_15 : x3 = 15
                                                · rw [dif_pos h3_15] at hc
                                                  subst x3
                                                  dsimp only at hc
                                                  cases tail3 with
                                                  | nil =>
                                                      dsimp only at hc
                                                      split at hc <;> contradiction
                                                  | cons _ _ =>
                                                      dsimp only at hc
                                                      contradiction
                                                · rw [dif_neg h3_15] at hc
                                                  contradiction
                                          · rw [dif_neg h2_3] at hc
                                            contradiction
                                    · rw [dif_neg h1_3] at hc
                                      by_cases h1_15 : x1 = 15
                                      · rw [dif_pos h1_15] at hc
                                        subst x1
                                        dsimp only at hc
                                        cases tail1 with
                                        | nil =>
                                            dsimp only at hc
                                            contradiction
                                        | cons x2 tail2 =>
                                            dsimp only at hc
                                            by_cases h2_3 : x2 = 3
                                            · rw [dif_pos h2_3] at hc
                                              subst x2
                                              dsimp only at hc
                                              cases tail2 with
                                              | nil =>
                                                  dsimp only at hc
                                                  contradiction
                                              | cons x3 tail3 =>
                                                  dsimp only at hc
                                                  by_cases h3_3 : x3 = 3
                                                  · rw [dif_pos h3_3] at hc
                                                    subst x3
                                                    dsimp only at hc
                                                    cases tail3 with
                                                    | nil =>
                                                        dsimp only at hc
                                                        split at hc <;> contradiction
                                                    | cons _ _ =>
                                                        dsimp only at hc
                                                        contradiction
                                                  · rw [dif_neg h3_3] at hc
                                                    contradiction
                                            · rw [dif_neg h2_3] at hc
                                              contradiction
                                      · rw [dif_neg h1_15] at hc
                                        contradiction
                              · rw [dif_neg h0_15] at hc
                                by_cases h0_16 : x0 = 16
                                · rw [dif_pos h0_16] at hc
                                  subst x0
                                  dsimp only at hc
                                  cases tail0 with
                                  | nil =>
                                      dsimp only at hc
                                      contradiction
                                  | cons x1 tail1 =>
                                      dsimp only at hc
                                      by_cases h1_9 : x1 = 9
                                      · rw [dif_pos h1_9] at hc
                                        subst x1
                                        dsimp only at hc
                                        cases tail1 with
                                        | nil =>
                                            dsimp only at hc
                                            contradiction
                                        | cons x2 tail2 =>
                                            dsimp only at hc
                                            by_cases h2_2 : x2 = 2
                                            · rw [dif_pos h2_2] at hc
                                              subst x2
                                              dsimp only at hc
                                              cases tail2 with
                                              | nil =>
                                                  dsimp only at hc
                                                  contradiction
                                              | cons x3 tail3 =>
                                                  dsimp only at hc
                                                  by_cases h3_9 : x3 = 9
                                                  · rw [dif_pos h3_9] at hc
                                                    subst x3
                                                    dsimp only at hc
                                                    cases tail3 with
                                                    | nil =>
                                                        dsimp only at hc
                                                        split at hc <;> contradiction
                                                    | cons _ _ =>
                                                        dsimp only at hc
                                                        contradiction
                                                  · rw [dif_neg h3_9] at hc
                                                    contradiction
                                            · rw [dif_neg h2_2] at hc
                                              contradiction
                                      · rw [dif_neg h1_9] at hc
                                        contradiction
                                · rw [dif_neg h0_16] at hc
                                  by_cases h0_17 : x0 = 17
                                  · rw [dif_pos h0_17] at hc
                                    subst x0
                                    dsimp only at hc
                                    cases tail0 with
                                    | nil =>
                                        dsimp only at hc
                                        contradiction
                                    | cons x1 tail1 =>
                                        dsimp only at hc
                                        by_cases h1_1 : x1 = 1
                                        · rw [dif_pos h1_1] at hc
                                          subst x1
                                          dsimp only at hc
                                          cases tail1 with
                                          | nil =>
                                              dsimp only at hc
                                              contradiction
                                          | cons x2 tail2 =>
                                              dsimp only at hc
                                              by_cases h2_1 : x2 = 1
                                              · rw [dif_pos h2_1] at hc
                                                subst x2
                                                dsimp only at hc
                                                cases tail2 with
                                                | nil =>
                                                    dsimp only at hc
                                                    contradiction
                                                | cons x3 tail3 =>
                                                    dsimp only at hc
                                                    by_cases h3_17 : x3 = 17
                                                    · rw [dif_pos h3_17] at hc
                                                      subst x3
                                                      dsimp only at hc
                                                      cases tail3 with
                                                      | nil =>
                                                          dsimp only at hc
                                                          split at hc <;> contradiction
                                                      | cons _ _ =>
                                                          dsimp only at hc
                                                          contradiction
                                                    · rw [dif_neg h3_17] at hc
                                                      contradiction
                                              · rw [dif_neg h2_1] at hc
                                                contradiction
                                        · rw [dif_neg h1_1] at hc
                                          by_cases h1_17 : x1 = 17
                                          · rw [dif_pos h1_17] at hc
                                            subst x1
                                            dsimp only at hc
                                            cases tail1 with
                                            | nil =>
                                                dsimp only at hc
                                                contradiction
                                            | cons x2 tail2 =>
                                                dsimp only at hc
                                                by_cases h2_1 : x2 = 1
                                                · rw [dif_pos h2_1] at hc
                                                  subst x2
                                                  dsimp only at hc
                                                  cases tail2 with
                                                  | nil =>
                                                      dsimp only at hc
                                                      contradiction
                                                  | cons x3 tail3 =>
                                                      dsimp only at hc
                                                      by_cases h3_1 : x3 = 1
                                                      · rw [dif_pos h3_1] at hc
                                                        subst x3
                                                        dsimp only at hc
                                                        cases tail3 with
                                                        | nil =>
                                                            dsimp only at hc
                                                            split at hc <;> contradiction
                                                        | cons _ _ =>
                                                            dsimp only at hc
                                                            contradiction
                                                      · rw [dif_neg h3_1] at hc
                                                        contradiction
                                                · rw [dif_neg h2_1] at hc
                                                  contradiction
                                          · rw [dif_neg h1_17] at hc
                                            contradiction
                                  · rw [dif_neg h0_17] at hc
                                    contradiction

end Agent1.Periodic

#print axioms Agent1.Periodic.outerComponent_eighteen_phase
