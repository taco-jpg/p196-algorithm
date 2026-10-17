import P196.Agent107FoldedTransducer.Agent107TransducerTablesChecks

namespace Agent107.FoldedTransducer.Table

set_option maxRecDepth 200000
set_option maxHeartbeats 0

theorem nodup_blocks {α β : Type} (key : α → β) (bs : List (β × List α))
    (hn : (bs.map Prod.fst).Nodup)
    (hr : ∀ b ∈ bs, b.2.Nodup ∧ ∀ x ∈ b.2, key x = b.1) :
    (bs.flatMap Prod.snd).Nodup := by
  induction bs with
  | nil => exact List.Pairwise.nil
  | cons b bs ih =>
    have hk := List.pairwise_cons.mp hn
    have hb := hr b (by simp)
    have ht : ∀ c ∈ bs, c.2.Nodup ∧ ∀ x ∈ c.2, key x = c.1 := by
      intro c hc
      exact hr c (List.mem_cons_of_mem _ hc)
    change (b.2 ++ bs.flatMap Prod.snd).Pairwise (fun x y => x ≠ y)
    apply List.pairwise_append.mpr
    refine ⟨hb.1, ih hk.2 ht, ?_⟩
    intro x hx y hy heq
    obtain ⟨c, hc, hy⟩ := List.mem_flatMap.mp hy
    have hne := hk.1 c.1 (List.mem_map.mpr ⟨c, hc, rfl⟩)
    exact hne ((hb.2 x hx).symm.trans ((congrArg key heq).trans ((ht c hc).2 y hy)))

def edgeBlocks : List (State × List Edge) := [(state0, edges0), (state1, edges1), (state2, edges2), (state3, edges3), (state4, edges4), (state5, edges5), (state6, edges6), (state7, edges7), (state8, edges8), (state9, edges9), (state10, edges10), (state11, edges11), (state12, edges12), (state13, edges13), (state14, edges14), (state15, edges15), (state16, edges16), (state17, edges17), (state18, edges18), (state19, edges19), (state20, edges20), (state21, edges21), (state22, edges22), (state23, edges23), (state24, edges24), (state25, edges25), (state26, edges26), (state27, edges27), (state28, edges28), (state29, edges29), (state30, edges30), (state31, edges31), (state32, edges32), (state33, edges33), (state34, edges34), (state35, edges35), (state36, edges36), (state37, edges37), (state38, edges38), (state39, edges39), (state40, edges40), (state41, edges41), (state42, edges42), (state43, edges43), (state44, edges44), (state45, edges45)]
def terminalBlocks : List (State × List TerminalRow) := [(state0, terminals0), (state1, terminals1), (state2, terminals2), (state3, terminals3), (state4, terminals4), (state5, terminals5), (state6, terminals6), (state7, terminals7), (state8, terminals8), (state9, terminals9), (state10, terminals10), (state11, terminals11), (state12, terminals12), (state13, terminals13), (state14, terminals14), (state15, terminals15), (state16, terminals16), (state17, terminals17), (state18, terminals18), (state19, terminals19), (state20, terminals20), (state21, terminals21), (state22, terminals22), (state23, terminals23), (state24, terminals24), (state25, terminals25), (state26, terminals26), (state27, terminals27), (state28, terminals28), (state29, terminals29), (state30, terminals30), (state31, terminals31), (state32, terminals32), (state33, terminals33), (state34, terminals34), (state35, terminals35), (state36, terminals36), (state37, terminals37), (state38, terminals38), (state39, terminals39), (state40, terminals40), (state41, terminals41), (state42, terminals42), (state43, terminals43), (state44, terminals44), (state45, terminals45)]

theorem edges_nodup : edges.Nodup := by
  change (edgeBlocks.flatMap Prod.snd).Nodup
  apply nodup_blocks Edge.source edgeBlocks
  · exact states_nodup
  · intro b hb
    simp only [edgeBlocks, List.mem_cons, List.mem_nil_iff, or_false] at hb
    rcases hb with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · exact row0_separated
    · exact row1_separated
    · exact row2_separated
    · exact row3_separated
    · exact row4_separated
    · exact row5_separated
    · exact row6_separated
    · exact row7_separated
    · exact row8_separated
    · exact row9_separated
    · exact row10_separated
    · exact row11_separated
    · exact row12_separated
    · exact row13_separated
    · exact row14_separated
    · exact row15_separated
    · exact row16_separated
    · exact row17_separated
    · exact row18_separated
    · exact row19_separated
    · exact row20_separated
    · exact row21_separated
    · exact row22_separated
    · exact row23_separated
    · exact row24_separated
    · exact row25_separated
    · exact row26_separated
    · exact row27_separated
    · exact row28_separated
    · exact row29_separated
    · exact row30_separated
    · exact row31_separated
    · exact row32_separated
    · exact row33_separated
    · exact row34_separated
    · exact row35_separated
    · exact row36_separated
    · exact row37_separated
    · exact row38_separated
    · exact row39_separated
    · exact row40_separated
    · exact row41_separated
    · exact row42_separated
    · exact row43_separated
    · exact row44_separated
    · exact row45_separated

theorem terminals_nodup : terminals.Nodup := by
  change (terminalBlocks.flatMap Prod.snd).Nodup
  apply nodup_blocks TerminalRow.source terminalBlocks
  · exact states_nodup
  · intro b hb
    simp only [terminalBlocks, List.mem_cons, List.mem_nil_iff, or_false] at hb
    rcases hb with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
    · exact terminal_row0_separated
    · exact terminal_row1_separated
    · exact terminal_row2_separated
    · exact terminal_row3_separated
    · exact terminal_row4_separated
    · exact terminal_row5_separated
    · exact terminal_row6_separated
    · exact terminal_row7_separated
    · exact terminal_row8_separated
    · exact terminal_row9_separated
    · exact terminal_row10_separated
    · exact terminal_row11_separated
    · exact terminal_row12_separated
    · exact terminal_row13_separated
    · exact terminal_row14_separated
    · exact terminal_row15_separated
    · exact terminal_row16_separated
    · exact terminal_row17_separated
    · exact terminal_row18_separated
    · exact terminal_row19_separated
    · exact terminal_row20_separated
    · exact terminal_row21_separated
    · exact terminal_row22_separated
    · exact terminal_row23_separated
    · exact terminal_row24_separated
    · exact terminal_row25_separated
    · exact terminal_row26_separated
    · exact terminal_row27_separated
    · exact terminal_row28_separated
    · exact terminal_row29_separated
    · exact terminal_row30_separated
    · exact terminal_row31_separated
    · exact terminal_row32_separated
    · exact terminal_row33_separated
    · exact terminal_row34_separated
    · exact terminal_row35_separated
    · exact terminal_row36_separated
    · exact terminal_row37_separated
    · exact terminal_row38_separated
    · exact terminal_row39_separated
    · exact terminal_row40_separated
    · exact terminal_row41_separated
    · exact terminal_row42_separated
    · exact terminal_row43_separated
    · exact terminal_row44_separated
    · exact terminal_row45_separated

theorem edge_sound (e : Edge) (he : e ∈ edges) :
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by
  obtain ⟨row, hr, he⟩ := List.mem_flatten.mp he
  simp only [edgeRows, List.mem_cons, List.mem_nil_iff, or_false] at hr
  rcases hr with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact row0_sound e he
  · exact row1_sound e he
  · exact row2_sound e he
  · exact row3_sound e he
  · exact row4_sound e he
  · exact row5_sound e he
  · exact row6_sound e he
  · exact row7_sound e he
  · exact row8_sound e he
  · exact row9_sound e he
  · exact row10_sound e he
  · exact row11_sound e he
  · exact row12_sound e he
  · exact row13_sound e he
  · exact row14_sound e he
  · exact row15_sound e he
  · exact row16_sound e he
  · exact row17_sound e he
  · exact row18_sound e he
  · exact row19_sound e he
  · exact row20_sound e he
  · exact row21_sound e he
  · exact row22_sound e he
  · exact row23_sound e he
  · exact row24_sound e he
  · exact row25_sound e he
  · exact row26_sound e he
  · exact row27_sound e he
  · exact row28_sound e he
  · exact row29_sound e he
  · exact row30_sound e he
  · exact row31_sound e he
  · exact row32_sound e he
  · exact row33_sound e he
  · exact row34_sound e he
  · exact row35_sound e he
  · exact row36_sound e he
  · exact row37_sound e he
  · exact row38_sound e he
  · exact row39_sound e he
  · exact row40_sound e he
  · exact row41_sound e he
  · exact row42_sound e he
  · exact row43_sound e he
  · exact row44_sound e he
  · exact row45_sound e he

theorem transition_complete (s t : State) (q : Nat)
    (hs : s ∈ states) (h : Transition s q t) :
    (⟨s, q, emit s q t.high, t⟩ : Edge) ∈ edges := by
  rcases h with ⟨hq, hstart, hb, hcarry, ht⟩
  have hqfin : q < 19 := by omega
  have hbfin : t.high < 2 := by omega
  simp only [states, List.mem_cons, List.mem_nil_iff, or_false] at hs
  rcases hs with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · have hc := row0_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges0, by simp [edgeRows], hc⟩
  · have hc := row1_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges1, by simp [edgeRows], hc⟩
  · have hc := row2_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges2, by simp [edgeRows], hc⟩
  · have hc := row3_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges3, by simp [edgeRows], hc⟩
  · have hc := row4_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges4, by simp [edgeRows], hc⟩
  · have hc := row5_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges5, by simp [edgeRows], hc⟩
  · have hc := row6_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges6, by simp [edgeRows], hc⟩
  · have hc := row7_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges7, by simp [edgeRows], hc⟩
  · have hc := row8_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges8, by simp [edgeRows], hc⟩
  · have hc := row9_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges9, by simp [edgeRows], hc⟩
  · have hc := row10_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges10, by simp [edgeRows], hc⟩
  · have hc := row11_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges11, by simp [edgeRows], hc⟩
  · have hc := row12_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges12, by simp [edgeRows], hc⟩
  · have hc := row13_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges13, by simp [edgeRows], hc⟩
  · have hc := row14_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges14, by simp [edgeRows], hc⟩
  · have hc := row15_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges15, by simp [edgeRows], hc⟩
  · have hc := row16_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges16, by simp [edgeRows], hc⟩
  · have hc := row17_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges17, by simp [edgeRows], hc⟩
  · have hc := row18_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges18, by simp [edgeRows], hc⟩
  · have hc := row19_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges19, by simp [edgeRows], hc⟩
  · have hc := row20_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges20, by simp [edgeRows], hc⟩
  · have hc := row21_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges21, by simp [edgeRows], hc⟩
  · have hc := row22_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges22, by simp [edgeRows], hc⟩
  · have hc := row23_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges23, by simp [edgeRows], hc⟩
  · have hc := row24_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges24, by simp [edgeRows], hc⟩
  · have hc := row25_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges25, by simp [edgeRows], hc⟩
  · have hc := row26_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges26, by simp [edgeRows], hc⟩
  · have hc := row27_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges27, by simp [edgeRows], hc⟩
  · have hc := row28_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges28, by simp [edgeRows], hc⟩
  · have hc := row29_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges29, by simp [edgeRows], hc⟩
  · have hc := row30_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges30, by simp [edgeRows], hc⟩
  · have hc := row31_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges31, by simp [edgeRows], hc⟩
  · have hc := row32_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges32, by simp [edgeRows], hc⟩
  · have hc := row33_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges33, by simp [edgeRows], hc⟩
  · have hc := row34_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges34, by simp [edgeRows], hc⟩
  · have hc := row35_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges35, by simp [edgeRows], hc⟩
  · have hc := row36_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges36, by simp [edgeRows], hc⟩
  · have hc := row37_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges37, by simp [edgeRows], hc⟩
  · have hc := row38_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges38, by simp [edgeRows], hc⟩
  · have hc := row39_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges39, by simp [edgeRows], hc⟩
  · have hc := row40_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges40, by simp [edgeRows], hc⟩
  · have hc := row41_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges41, by simp [edgeRows], hc⟩
  · have hc := row42_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges42, by simp [edgeRows], hc⟩
  · have hc := row43_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges43, by simp [edgeRows], hc⟩
  · have hc := row44_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges44, by simp [edgeRows], hc⟩
  · have hc := row45_complete ⟨q, hqfin⟩ ⟨t.high, hbfin⟩ hstart hcarry
    change (⟨_, q, _, nextState _ q t.high⟩ : Edge) ∈ _ at hc
    rw [← ht] at hc
    exact List.mem_flatten.mpr ⟨edges45, by simp [edgeRows], hc⟩

theorem states_closed (s t : State) (q : Nat) (hs : s ∈ states)
    (h : Transition s q t) : t ∈ states :=
  (edge_sound _ (transition_complete s t q hs h)).2.1

theorem terminal_sound (r : TerminalRow) (hr : r ∈ terminals) :
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by
  obtain ⟨row, hrow, hr⟩ := List.mem_flatten.mp hr
  simp only [terminalRows, List.mem_cons, List.mem_nil_iff, or_false] at hrow
  rcases hrow with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact terminal_row0_sound r hr
  · exact terminal_row1_sound r hr
  · exact terminal_row2_sound r hr
  · exact terminal_row3_sound r hr
  · exact terminal_row4_sound r hr
  · exact terminal_row5_sound r hr
  · exact terminal_row6_sound r hr
  · exact terminal_row7_sound r hr
  · exact terminal_row8_sound r hr
  · exact terminal_row9_sound r hr
  · exact terminal_row10_sound r hr
  · exact terminal_row11_sound r hr
  · exact terminal_row12_sound r hr
  · exact terminal_row13_sound r hr
  · exact terminal_row14_sound r hr
  · exact terminal_row15_sound r hr
  · exact terminal_row16_sound r hr
  · exact terminal_row17_sound r hr
  · exact terminal_row18_sound r hr
  · exact terminal_row19_sound r hr
  · exact terminal_row20_sound r hr
  · exact terminal_row21_sound r hr
  · exact terminal_row22_sound r hr
  · exact terminal_row23_sound r hr
  · exact terminal_row24_sound r hr
  · exact terminal_row25_sound r hr
  · exact terminal_row26_sound r hr
  · exact terminal_row27_sound r hr
  · exact terminal_row28_sound r hr
  · exact terminal_row29_sound r hr
  · exact terminal_row30_sound r hr
  · exact terminal_row31_sound r hr
  · exact terminal_row32_sound r hr
  · exact terminal_row33_sound r hr
  · exact terminal_row34_sound r hr
  · exact terminal_row35_sound r hr
  · exact terminal_row36_sound r hr
  · exact terminal_row37_sound r hr
  · exact terminal_row38_sound r hr
  · exact terminal_row39_sound r hr
  · exact terminal_row40_sound r hr
  · exact terminal_row41_sound r hr
  · exact terminal_row42_sound r hr
  · exact terminal_row43_sound r hr
  · exact terminal_row44_sound r hr
  · exact terminal_row45_sound r hr

theorem terminal_center_mem (s : State) (c : Option Nat) (h : Terminal s c) : c ∈ centers := by
  cases c with
  | none => simp [centers]
  | some v =>
    have hv : v ≤ 18 := h.2.1
    simp only [centers, List.mem_cons, Option.some.injEq, List.mem_map]
    exact Or.inr ⟨v, List.mem_range.mpr (by omega), rfl⟩

theorem terminal_complete (s : State) (c : Option Nat)
    (hs : s ∈ states) (h : Terminal s c) :
    (⟨s, c, terminalExtra s c, terminalCenter s c⟩ : TerminalRow) ∈ terminals := by
  have hc := terminal_center_mem s c h
  simp only [states, List.mem_cons, List.mem_nil_iff, or_false] at hs
  rcases hs with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact List.mem_flatten.mpr ⟨terminals0, by simp [terminalRows], terminal_row0_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals1, by simp [terminalRows], terminal_row1_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals2, by simp [terminalRows], terminal_row2_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals3, by simp [terminalRows], terminal_row3_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals4, by simp [terminalRows], terminal_row4_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals5, by simp [terminalRows], terminal_row5_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals6, by simp [terminalRows], terminal_row6_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals7, by simp [terminalRows], terminal_row7_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals8, by simp [terminalRows], terminal_row8_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals9, by simp [terminalRows], terminal_row9_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals10, by simp [terminalRows], terminal_row10_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals11, by simp [terminalRows], terminal_row11_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals12, by simp [terminalRows], terminal_row12_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals13, by simp [terminalRows], terminal_row13_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals14, by simp [terminalRows], terminal_row14_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals15, by simp [terminalRows], terminal_row15_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals16, by simp [terminalRows], terminal_row16_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals17, by simp [terminalRows], terminal_row17_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals18, by simp [terminalRows], terminal_row18_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals19, by simp [terminalRows], terminal_row19_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals20, by simp [terminalRows], terminal_row20_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals21, by simp [terminalRows], terminal_row21_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals22, by simp [terminalRows], terminal_row22_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals23, by simp [terminalRows], terminal_row23_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals24, by simp [terminalRows], terminal_row24_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals25, by simp [terminalRows], terminal_row25_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals26, by simp [terminalRows], terminal_row26_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals27, by simp [terminalRows], terminal_row27_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals28, by simp [terminalRows], terminal_row28_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals29, by simp [terminalRows], terminal_row29_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals30, by simp [terminalRows], terminal_row30_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals31, by simp [terminalRows], terminal_row31_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals32, by simp [terminalRows], terminal_row32_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals33, by simp [terminalRows], terminal_row33_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals34, by simp [terminalRows], terminal_row34_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals35, by simp [terminalRows], terminal_row35_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals36, by simp [terminalRows], terminal_row36_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals37, by simp [terminalRows], terminal_row37_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals38, by simp [terminalRows], terminal_row38_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals39, by simp [terminalRows], terminal_row39_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals40, by simp [terminalRows], terminal_row40_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals41, by simp [terminalRows], terminal_row41_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals42, by simp [terminalRows], terminal_row42_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals43, by simp [terminalRows], terminal_row43_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals44, by simp [terminalRows], terminal_row44_complete c hc h⟩
  · exact List.mem_flatten.mpr ⟨terminals45, by simp [terminalRows], terminal_row45_complete c hc h⟩

theorem edge_mem_iff (s t : State) (q o : Nat) :
    (⟨s, q, o, t⟩ : Edge) ∈ edges ↔
      s ∈ states ∧ Transition s q t ∧ o = emit s q t.high := by
  constructor
  · intro h
    have he := edge_sound _ h
    exact ⟨he.1, he.2.2.1, he.2.2.2⟩
  · rintro ⟨hs, h, rfl⟩
    exact transition_complete s t q hs h

theorem terminal_mem_iff (s : State) (c extra oc : Option Nat) :
    (⟨s, c, extra, oc⟩ : TerminalRow) ∈ terminals ↔
      s ∈ states ∧ Terminal s c ∧ extra = terminalExtra s c ∧ oc = terminalCenter s c := by
  constructor
  · intro h
    exact terminal_sound _ h
  · rintro ⟨hs, h, rfl, rfl⟩
    exact terminal_complete s c hs h

#print axioms states_nodup
#print axioms edges_nodup
#print axioms terminals_nodup
#print axioms starts_mem
#print axioms edge_sound
#print axioms transition_complete
#print axioms states_closed
#print axioms terminal_sound
#print axioms terminal_complete
#print axioms edge_mem_iff
#print axioms terminal_mem_iff

end Agent107.FoldedTransducer.Table
