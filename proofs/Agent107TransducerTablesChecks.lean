import Agent107TransducerTablesData

namespace Agent107.FoldedTransducer.Table

set_option maxRecDepth 200000
set_option maxHeartbeats 0

theorem row0_separated : edges0.Nodup ∧ ∀ e ∈ edges0, e.source = state0 := by decide
theorem terminal_row0_separated : terminals0.Nodup ∧ ∀ r ∈ terminals0, r.source = state0 := by decide

theorem row0_sound : ∀ e ∈ edges0,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row0_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state0.started = false → 0 < q.val) → (q.val + b.val) / 10 = state0.high →
    (⟨state0, q.val, emit state0 q.val b.val, nextState state0 q.val b.val⟩ : Edge) ∈ edges0 := by decide

theorem terminal_row0_sound : ∀ r ∈ terminals0,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row0_complete : ∀ c ∈ centers, Terminal state0 c →
    (⟨state0, c, terminalExtra state0 c, terminalCenter state0 c⟩ : TerminalRow) ∈ terminals0 := by decide

theorem row1_separated : edges1.Nodup ∧ ∀ e ∈ edges1, e.source = state1 := by decide
theorem terminal_row1_separated : terminals1.Nodup ∧ ∀ r ∈ terminals1, r.source = state1 := by decide

theorem row1_sound : ∀ e ∈ edges1,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row1_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state1.started = false → 0 < q.val) → (q.val + b.val) / 10 = state1.high →
    (⟨state1, q.val, emit state1 q.val b.val, nextState state1 q.val b.val⟩ : Edge) ∈ edges1 := by decide

theorem terminal_row1_sound : ∀ r ∈ terminals1,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row1_complete : ∀ c ∈ centers, Terminal state1 c →
    (⟨state1, c, terminalExtra state1 c, terminalCenter state1 c⟩ : TerminalRow) ∈ terminals1 := by decide

theorem row2_separated : edges2.Nodup ∧ ∀ e ∈ edges2, e.source = state2 := by decide
theorem terminal_row2_separated : terminals2.Nodup ∧ ∀ r ∈ terminals2, r.source = state2 := by decide

theorem row2_sound : ∀ e ∈ edges2,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row2_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state2.started = false → 0 < q.val) → (q.val + b.val) / 10 = state2.high →
    (⟨state2, q.val, emit state2 q.val b.val, nextState state2 q.val b.val⟩ : Edge) ∈ edges2 := by decide

theorem terminal_row2_sound : ∀ r ∈ terminals2,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row2_complete : ∀ c ∈ centers, Terminal state2 c →
    (⟨state2, c, terminalExtra state2 c, terminalCenter state2 c⟩ : TerminalRow) ∈ terminals2 := by decide

theorem row3_separated : edges3.Nodup ∧ ∀ e ∈ edges3, e.source = state3 := by decide
theorem terminal_row3_separated : terminals3.Nodup ∧ ∀ r ∈ terminals3, r.source = state3 := by decide

theorem row3_sound : ∀ e ∈ edges3,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row3_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state3.started = false → 0 < q.val) → (q.val + b.val) / 10 = state3.high →
    (⟨state3, q.val, emit state3 q.val b.val, nextState state3 q.val b.val⟩ : Edge) ∈ edges3 := by decide

theorem terminal_row3_sound : ∀ r ∈ terminals3,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row3_complete : ∀ c ∈ centers, Terminal state3 c →
    (⟨state3, c, terminalExtra state3 c, terminalCenter state3 c⟩ : TerminalRow) ∈ terminals3 := by decide

theorem row4_separated : edges4.Nodup ∧ ∀ e ∈ edges4, e.source = state4 := by decide
theorem terminal_row4_separated : terminals4.Nodup ∧ ∀ r ∈ terminals4, r.source = state4 := by decide

theorem row4_sound : ∀ e ∈ edges4,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row4_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state4.started = false → 0 < q.val) → (q.val + b.val) / 10 = state4.high →
    (⟨state4, q.val, emit state4 q.val b.val, nextState state4 q.val b.val⟩ : Edge) ∈ edges4 := by decide

theorem terminal_row4_sound : ∀ r ∈ terminals4,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row4_complete : ∀ c ∈ centers, Terminal state4 c →
    (⟨state4, c, terminalExtra state4 c, terminalCenter state4 c⟩ : TerminalRow) ∈ terminals4 := by decide

theorem row5_separated : edges5.Nodup ∧ ∀ e ∈ edges5, e.source = state5 := by decide
theorem terminal_row5_separated : terminals5.Nodup ∧ ∀ r ∈ terminals5, r.source = state5 := by decide

theorem row5_sound : ∀ e ∈ edges5,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row5_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state5.started = false → 0 < q.val) → (q.val + b.val) / 10 = state5.high →
    (⟨state5, q.val, emit state5 q.val b.val, nextState state5 q.val b.val⟩ : Edge) ∈ edges5 := by decide

theorem terminal_row5_sound : ∀ r ∈ terminals5,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row5_complete : ∀ c ∈ centers, Terminal state5 c →
    (⟨state5, c, terminalExtra state5 c, terminalCenter state5 c⟩ : TerminalRow) ∈ terminals5 := by decide

theorem row6_separated : edges6.Nodup ∧ ∀ e ∈ edges6, e.source = state6 := by decide
theorem terminal_row6_separated : terminals6.Nodup ∧ ∀ r ∈ terminals6, r.source = state6 := by decide

theorem row6_sound : ∀ e ∈ edges6,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row6_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state6.started = false → 0 < q.val) → (q.val + b.val) / 10 = state6.high →
    (⟨state6, q.val, emit state6 q.val b.val, nextState state6 q.val b.val⟩ : Edge) ∈ edges6 := by decide

theorem terminal_row6_sound : ∀ r ∈ terminals6,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row6_complete : ∀ c ∈ centers, Terminal state6 c →
    (⟨state6, c, terminalExtra state6 c, terminalCenter state6 c⟩ : TerminalRow) ∈ terminals6 := by decide

theorem row7_separated : edges7.Nodup ∧ ∀ e ∈ edges7, e.source = state7 := by decide
theorem terminal_row7_separated : terminals7.Nodup ∧ ∀ r ∈ terminals7, r.source = state7 := by decide

theorem row7_sound : ∀ e ∈ edges7,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row7_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state7.started = false → 0 < q.val) → (q.val + b.val) / 10 = state7.high →
    (⟨state7, q.val, emit state7 q.val b.val, nextState state7 q.val b.val⟩ : Edge) ∈ edges7 := by decide

theorem terminal_row7_sound : ∀ r ∈ terminals7,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row7_complete : ∀ c ∈ centers, Terminal state7 c →
    (⟨state7, c, terminalExtra state7 c, terminalCenter state7 c⟩ : TerminalRow) ∈ terminals7 := by decide

theorem row8_separated : edges8.Nodup ∧ ∀ e ∈ edges8, e.source = state8 := by decide
theorem terminal_row8_separated : terminals8.Nodup ∧ ∀ r ∈ terminals8, r.source = state8 := by decide

theorem row8_sound : ∀ e ∈ edges8,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row8_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state8.started = false → 0 < q.val) → (q.val + b.val) / 10 = state8.high →
    (⟨state8, q.val, emit state8 q.val b.val, nextState state8 q.val b.val⟩ : Edge) ∈ edges8 := by decide

theorem terminal_row8_sound : ∀ r ∈ terminals8,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row8_complete : ∀ c ∈ centers, Terminal state8 c →
    (⟨state8, c, terminalExtra state8 c, terminalCenter state8 c⟩ : TerminalRow) ∈ terminals8 := by decide

theorem row9_separated : edges9.Nodup ∧ ∀ e ∈ edges9, e.source = state9 := by decide
theorem terminal_row9_separated : terminals9.Nodup ∧ ∀ r ∈ terminals9, r.source = state9 := by decide

theorem row9_sound : ∀ e ∈ edges9,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row9_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state9.started = false → 0 < q.val) → (q.val + b.val) / 10 = state9.high →
    (⟨state9, q.val, emit state9 q.val b.val, nextState state9 q.val b.val⟩ : Edge) ∈ edges9 := by decide

theorem terminal_row9_sound : ∀ r ∈ terminals9,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row9_complete : ∀ c ∈ centers, Terminal state9 c →
    (⟨state9, c, terminalExtra state9 c, terminalCenter state9 c⟩ : TerminalRow) ∈ terminals9 := by decide

theorem row10_separated : edges10.Nodup ∧ ∀ e ∈ edges10, e.source = state10 := by decide
theorem terminal_row10_separated : terminals10.Nodup ∧ ∀ r ∈ terminals10, r.source = state10 := by decide

theorem row10_sound : ∀ e ∈ edges10,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row10_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state10.started = false → 0 < q.val) → (q.val + b.val) / 10 = state10.high →
    (⟨state10, q.val, emit state10 q.val b.val, nextState state10 q.val b.val⟩ : Edge) ∈ edges10 := by decide

theorem terminal_row10_sound : ∀ r ∈ terminals10,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row10_complete : ∀ c ∈ centers, Terminal state10 c →
    (⟨state10, c, terminalExtra state10 c, terminalCenter state10 c⟩ : TerminalRow) ∈ terminals10 := by decide

theorem row11_separated : edges11.Nodup ∧ ∀ e ∈ edges11, e.source = state11 := by decide
theorem terminal_row11_separated : terminals11.Nodup ∧ ∀ r ∈ terminals11, r.source = state11 := by decide

theorem row11_sound : ∀ e ∈ edges11,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row11_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state11.started = false → 0 < q.val) → (q.val + b.val) / 10 = state11.high →
    (⟨state11, q.val, emit state11 q.val b.val, nextState state11 q.val b.val⟩ : Edge) ∈ edges11 := by decide

theorem terminal_row11_sound : ∀ r ∈ terminals11,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row11_complete : ∀ c ∈ centers, Terminal state11 c →
    (⟨state11, c, terminalExtra state11 c, terminalCenter state11 c⟩ : TerminalRow) ∈ terminals11 := by decide

theorem row12_separated : edges12.Nodup ∧ ∀ e ∈ edges12, e.source = state12 := by decide
theorem terminal_row12_separated : terminals12.Nodup ∧ ∀ r ∈ terminals12, r.source = state12 := by decide

theorem row12_sound : ∀ e ∈ edges12,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row12_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state12.started = false → 0 < q.val) → (q.val + b.val) / 10 = state12.high →
    (⟨state12, q.val, emit state12 q.val b.val, nextState state12 q.val b.val⟩ : Edge) ∈ edges12 := by decide

theorem terminal_row12_sound : ∀ r ∈ terminals12,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row12_complete : ∀ c ∈ centers, Terminal state12 c →
    (⟨state12, c, terminalExtra state12 c, terminalCenter state12 c⟩ : TerminalRow) ∈ terminals12 := by decide

theorem row13_separated : edges13.Nodup ∧ ∀ e ∈ edges13, e.source = state13 := by decide
theorem terminal_row13_separated : terminals13.Nodup ∧ ∀ r ∈ terminals13, r.source = state13 := by decide

theorem row13_sound : ∀ e ∈ edges13,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row13_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state13.started = false → 0 < q.val) → (q.val + b.val) / 10 = state13.high →
    (⟨state13, q.val, emit state13 q.val b.val, nextState state13 q.val b.val⟩ : Edge) ∈ edges13 := by decide

theorem terminal_row13_sound : ∀ r ∈ terminals13,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row13_complete : ∀ c ∈ centers, Terminal state13 c →
    (⟨state13, c, terminalExtra state13 c, terminalCenter state13 c⟩ : TerminalRow) ∈ terminals13 := by decide

theorem row14_separated : edges14.Nodup ∧ ∀ e ∈ edges14, e.source = state14 := by decide
theorem terminal_row14_separated : terminals14.Nodup ∧ ∀ r ∈ terminals14, r.source = state14 := by decide

theorem row14_sound : ∀ e ∈ edges14,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row14_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state14.started = false → 0 < q.val) → (q.val + b.val) / 10 = state14.high →
    (⟨state14, q.val, emit state14 q.val b.val, nextState state14 q.val b.val⟩ : Edge) ∈ edges14 := by decide

theorem terminal_row14_sound : ∀ r ∈ terminals14,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row14_complete : ∀ c ∈ centers, Terminal state14 c →
    (⟨state14, c, terminalExtra state14 c, terminalCenter state14 c⟩ : TerminalRow) ∈ terminals14 := by decide

theorem row15_separated : edges15.Nodup ∧ ∀ e ∈ edges15, e.source = state15 := by decide
theorem terminal_row15_separated : terminals15.Nodup ∧ ∀ r ∈ terminals15, r.source = state15 := by decide

theorem row15_sound : ∀ e ∈ edges15,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row15_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state15.started = false → 0 < q.val) → (q.val + b.val) / 10 = state15.high →
    (⟨state15, q.val, emit state15 q.val b.val, nextState state15 q.val b.val⟩ : Edge) ∈ edges15 := by decide

theorem terminal_row15_sound : ∀ r ∈ terminals15,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row15_complete : ∀ c ∈ centers, Terminal state15 c →
    (⟨state15, c, terminalExtra state15 c, terminalCenter state15 c⟩ : TerminalRow) ∈ terminals15 := by decide

theorem row16_separated : edges16.Nodup ∧ ∀ e ∈ edges16, e.source = state16 := by decide
theorem terminal_row16_separated : terminals16.Nodup ∧ ∀ r ∈ terminals16, r.source = state16 := by decide

theorem row16_sound : ∀ e ∈ edges16,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row16_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state16.started = false → 0 < q.val) → (q.val + b.val) / 10 = state16.high →
    (⟨state16, q.val, emit state16 q.val b.val, nextState state16 q.val b.val⟩ : Edge) ∈ edges16 := by decide

theorem terminal_row16_sound : ∀ r ∈ terminals16,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row16_complete : ∀ c ∈ centers, Terminal state16 c →
    (⟨state16, c, terminalExtra state16 c, terminalCenter state16 c⟩ : TerminalRow) ∈ terminals16 := by decide

theorem row17_separated : edges17.Nodup ∧ ∀ e ∈ edges17, e.source = state17 := by decide
theorem terminal_row17_separated : terminals17.Nodup ∧ ∀ r ∈ terminals17, r.source = state17 := by decide

theorem row17_sound : ∀ e ∈ edges17,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row17_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state17.started = false → 0 < q.val) → (q.val + b.val) / 10 = state17.high →
    (⟨state17, q.val, emit state17 q.val b.val, nextState state17 q.val b.val⟩ : Edge) ∈ edges17 := by decide

theorem terminal_row17_sound : ∀ r ∈ terminals17,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row17_complete : ∀ c ∈ centers, Terminal state17 c →
    (⟨state17, c, terminalExtra state17 c, terminalCenter state17 c⟩ : TerminalRow) ∈ terminals17 := by decide

theorem row18_separated : edges18.Nodup ∧ ∀ e ∈ edges18, e.source = state18 := by decide
theorem terminal_row18_separated : terminals18.Nodup ∧ ∀ r ∈ terminals18, r.source = state18 := by decide

theorem row18_sound : ∀ e ∈ edges18,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row18_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state18.started = false → 0 < q.val) → (q.val + b.val) / 10 = state18.high →
    (⟨state18, q.val, emit state18 q.val b.val, nextState state18 q.val b.val⟩ : Edge) ∈ edges18 := by decide

theorem terminal_row18_sound : ∀ r ∈ terminals18,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row18_complete : ∀ c ∈ centers, Terminal state18 c →
    (⟨state18, c, terminalExtra state18 c, terminalCenter state18 c⟩ : TerminalRow) ∈ terminals18 := by decide

theorem row19_separated : edges19.Nodup ∧ ∀ e ∈ edges19, e.source = state19 := by decide
theorem terminal_row19_separated : terminals19.Nodup ∧ ∀ r ∈ terminals19, r.source = state19 := by decide

theorem row19_sound : ∀ e ∈ edges19,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row19_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state19.started = false → 0 < q.val) → (q.val + b.val) / 10 = state19.high →
    (⟨state19, q.val, emit state19 q.val b.val, nextState state19 q.val b.val⟩ : Edge) ∈ edges19 := by decide

theorem terminal_row19_sound : ∀ r ∈ terminals19,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row19_complete : ∀ c ∈ centers, Terminal state19 c →
    (⟨state19, c, terminalExtra state19 c, terminalCenter state19 c⟩ : TerminalRow) ∈ terminals19 := by decide

theorem row20_separated : edges20.Nodup ∧ ∀ e ∈ edges20, e.source = state20 := by decide
theorem terminal_row20_separated : terminals20.Nodup ∧ ∀ r ∈ terminals20, r.source = state20 := by decide

theorem row20_sound : ∀ e ∈ edges20,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row20_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state20.started = false → 0 < q.val) → (q.val + b.val) / 10 = state20.high →
    (⟨state20, q.val, emit state20 q.val b.val, nextState state20 q.val b.val⟩ : Edge) ∈ edges20 := by decide

theorem terminal_row20_sound : ∀ r ∈ terminals20,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row20_complete : ∀ c ∈ centers, Terminal state20 c →
    (⟨state20, c, terminalExtra state20 c, terminalCenter state20 c⟩ : TerminalRow) ∈ terminals20 := by decide

theorem row21_separated : edges21.Nodup ∧ ∀ e ∈ edges21, e.source = state21 := by decide
theorem terminal_row21_separated : terminals21.Nodup ∧ ∀ r ∈ terminals21, r.source = state21 := by decide

theorem row21_sound : ∀ e ∈ edges21,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row21_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state21.started = false → 0 < q.val) → (q.val + b.val) / 10 = state21.high →
    (⟨state21, q.val, emit state21 q.val b.val, nextState state21 q.val b.val⟩ : Edge) ∈ edges21 := by decide

theorem terminal_row21_sound : ∀ r ∈ terminals21,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row21_complete : ∀ c ∈ centers, Terminal state21 c →
    (⟨state21, c, terminalExtra state21 c, terminalCenter state21 c⟩ : TerminalRow) ∈ terminals21 := by decide

theorem row22_separated : edges22.Nodup ∧ ∀ e ∈ edges22, e.source = state22 := by decide
theorem terminal_row22_separated : terminals22.Nodup ∧ ∀ r ∈ terminals22, r.source = state22 := by decide

theorem row22_sound : ∀ e ∈ edges22,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row22_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state22.started = false → 0 < q.val) → (q.val + b.val) / 10 = state22.high →
    (⟨state22, q.val, emit state22 q.val b.val, nextState state22 q.val b.val⟩ : Edge) ∈ edges22 := by decide

theorem terminal_row22_sound : ∀ r ∈ terminals22,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row22_complete : ∀ c ∈ centers, Terminal state22 c →
    (⟨state22, c, terminalExtra state22 c, terminalCenter state22 c⟩ : TerminalRow) ∈ terminals22 := by decide

theorem row23_separated : edges23.Nodup ∧ ∀ e ∈ edges23, e.source = state23 := by decide
theorem terminal_row23_separated : terminals23.Nodup ∧ ∀ r ∈ terminals23, r.source = state23 := by decide

theorem row23_sound : ∀ e ∈ edges23,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row23_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state23.started = false → 0 < q.val) → (q.val + b.val) / 10 = state23.high →
    (⟨state23, q.val, emit state23 q.val b.val, nextState state23 q.val b.val⟩ : Edge) ∈ edges23 := by decide

theorem terminal_row23_sound : ∀ r ∈ terminals23,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row23_complete : ∀ c ∈ centers, Terminal state23 c →
    (⟨state23, c, terminalExtra state23 c, terminalCenter state23 c⟩ : TerminalRow) ∈ terminals23 := by decide

theorem row24_separated : edges24.Nodup ∧ ∀ e ∈ edges24, e.source = state24 := by decide
theorem terminal_row24_separated : terminals24.Nodup ∧ ∀ r ∈ terminals24, r.source = state24 := by decide

theorem row24_sound : ∀ e ∈ edges24,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row24_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state24.started = false → 0 < q.val) → (q.val + b.val) / 10 = state24.high →
    (⟨state24, q.val, emit state24 q.val b.val, nextState state24 q.val b.val⟩ : Edge) ∈ edges24 := by decide

theorem terminal_row24_sound : ∀ r ∈ terminals24,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row24_complete : ∀ c ∈ centers, Terminal state24 c →
    (⟨state24, c, terminalExtra state24 c, terminalCenter state24 c⟩ : TerminalRow) ∈ terminals24 := by decide

theorem row25_separated : edges25.Nodup ∧ ∀ e ∈ edges25, e.source = state25 := by decide
theorem terminal_row25_separated : terminals25.Nodup ∧ ∀ r ∈ terminals25, r.source = state25 := by decide

theorem row25_sound : ∀ e ∈ edges25,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row25_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state25.started = false → 0 < q.val) → (q.val + b.val) / 10 = state25.high →
    (⟨state25, q.val, emit state25 q.val b.val, nextState state25 q.val b.val⟩ : Edge) ∈ edges25 := by decide

theorem terminal_row25_sound : ∀ r ∈ terminals25,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row25_complete : ∀ c ∈ centers, Terminal state25 c →
    (⟨state25, c, terminalExtra state25 c, terminalCenter state25 c⟩ : TerminalRow) ∈ terminals25 := by decide

theorem row26_separated : edges26.Nodup ∧ ∀ e ∈ edges26, e.source = state26 := by decide
theorem terminal_row26_separated : terminals26.Nodup ∧ ∀ r ∈ terminals26, r.source = state26 := by decide

theorem row26_sound : ∀ e ∈ edges26,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row26_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state26.started = false → 0 < q.val) → (q.val + b.val) / 10 = state26.high →
    (⟨state26, q.val, emit state26 q.val b.val, nextState state26 q.val b.val⟩ : Edge) ∈ edges26 := by decide

theorem terminal_row26_sound : ∀ r ∈ terminals26,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row26_complete : ∀ c ∈ centers, Terminal state26 c →
    (⟨state26, c, terminalExtra state26 c, terminalCenter state26 c⟩ : TerminalRow) ∈ terminals26 := by decide

theorem row27_separated : edges27.Nodup ∧ ∀ e ∈ edges27, e.source = state27 := by decide
theorem terminal_row27_separated : terminals27.Nodup ∧ ∀ r ∈ terminals27, r.source = state27 := by decide

theorem row27_sound : ∀ e ∈ edges27,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row27_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state27.started = false → 0 < q.val) → (q.val + b.val) / 10 = state27.high →
    (⟨state27, q.val, emit state27 q.val b.val, nextState state27 q.val b.val⟩ : Edge) ∈ edges27 := by decide

theorem terminal_row27_sound : ∀ r ∈ terminals27,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row27_complete : ∀ c ∈ centers, Terminal state27 c →
    (⟨state27, c, terminalExtra state27 c, terminalCenter state27 c⟩ : TerminalRow) ∈ terminals27 := by decide

theorem row28_separated : edges28.Nodup ∧ ∀ e ∈ edges28, e.source = state28 := by decide
theorem terminal_row28_separated : terminals28.Nodup ∧ ∀ r ∈ terminals28, r.source = state28 := by decide

theorem row28_sound : ∀ e ∈ edges28,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row28_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state28.started = false → 0 < q.val) → (q.val + b.val) / 10 = state28.high →
    (⟨state28, q.val, emit state28 q.val b.val, nextState state28 q.val b.val⟩ : Edge) ∈ edges28 := by decide

theorem terminal_row28_sound : ∀ r ∈ terminals28,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row28_complete : ∀ c ∈ centers, Terminal state28 c →
    (⟨state28, c, terminalExtra state28 c, terminalCenter state28 c⟩ : TerminalRow) ∈ terminals28 := by decide

theorem row29_separated : edges29.Nodup ∧ ∀ e ∈ edges29, e.source = state29 := by decide
theorem terminal_row29_separated : terminals29.Nodup ∧ ∀ r ∈ terminals29, r.source = state29 := by decide

theorem row29_sound : ∀ e ∈ edges29,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row29_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state29.started = false → 0 < q.val) → (q.val + b.val) / 10 = state29.high →
    (⟨state29, q.val, emit state29 q.val b.val, nextState state29 q.val b.val⟩ : Edge) ∈ edges29 := by decide

theorem terminal_row29_sound : ∀ r ∈ terminals29,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row29_complete : ∀ c ∈ centers, Terminal state29 c →
    (⟨state29, c, terminalExtra state29 c, terminalCenter state29 c⟩ : TerminalRow) ∈ terminals29 := by decide

theorem row30_separated : edges30.Nodup ∧ ∀ e ∈ edges30, e.source = state30 := by decide
theorem terminal_row30_separated : terminals30.Nodup ∧ ∀ r ∈ terminals30, r.source = state30 := by decide

theorem row30_sound : ∀ e ∈ edges30,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row30_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state30.started = false → 0 < q.val) → (q.val + b.val) / 10 = state30.high →
    (⟨state30, q.val, emit state30 q.val b.val, nextState state30 q.val b.val⟩ : Edge) ∈ edges30 := by decide

theorem terminal_row30_sound : ∀ r ∈ terminals30,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row30_complete : ∀ c ∈ centers, Terminal state30 c →
    (⟨state30, c, terminalExtra state30 c, terminalCenter state30 c⟩ : TerminalRow) ∈ terminals30 := by decide

theorem row31_separated : edges31.Nodup ∧ ∀ e ∈ edges31, e.source = state31 := by decide
theorem terminal_row31_separated : terminals31.Nodup ∧ ∀ r ∈ terminals31, r.source = state31 := by decide

theorem row31_sound : ∀ e ∈ edges31,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row31_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state31.started = false → 0 < q.val) → (q.val + b.val) / 10 = state31.high →
    (⟨state31, q.val, emit state31 q.val b.val, nextState state31 q.val b.val⟩ : Edge) ∈ edges31 := by decide

theorem terminal_row31_sound : ∀ r ∈ terminals31,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row31_complete : ∀ c ∈ centers, Terminal state31 c →
    (⟨state31, c, terminalExtra state31 c, terminalCenter state31 c⟩ : TerminalRow) ∈ terminals31 := by decide

theorem row32_separated : edges32.Nodup ∧ ∀ e ∈ edges32, e.source = state32 := by decide
theorem terminal_row32_separated : terminals32.Nodup ∧ ∀ r ∈ terminals32, r.source = state32 := by decide

theorem row32_sound : ∀ e ∈ edges32,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row32_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state32.started = false → 0 < q.val) → (q.val + b.val) / 10 = state32.high →
    (⟨state32, q.val, emit state32 q.val b.val, nextState state32 q.val b.val⟩ : Edge) ∈ edges32 := by decide

theorem terminal_row32_sound : ∀ r ∈ terminals32,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row32_complete : ∀ c ∈ centers, Terminal state32 c →
    (⟨state32, c, terminalExtra state32 c, terminalCenter state32 c⟩ : TerminalRow) ∈ terminals32 := by decide

theorem row33_separated : edges33.Nodup ∧ ∀ e ∈ edges33, e.source = state33 := by decide
theorem terminal_row33_separated : terminals33.Nodup ∧ ∀ r ∈ terminals33, r.source = state33 := by decide

theorem row33_sound : ∀ e ∈ edges33,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row33_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state33.started = false → 0 < q.val) → (q.val + b.val) / 10 = state33.high →
    (⟨state33, q.val, emit state33 q.val b.val, nextState state33 q.val b.val⟩ : Edge) ∈ edges33 := by decide

theorem terminal_row33_sound : ∀ r ∈ terminals33,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row33_complete : ∀ c ∈ centers, Terminal state33 c →
    (⟨state33, c, terminalExtra state33 c, terminalCenter state33 c⟩ : TerminalRow) ∈ terminals33 := by decide

theorem row34_separated : edges34.Nodup ∧ ∀ e ∈ edges34, e.source = state34 := by decide
theorem terminal_row34_separated : terminals34.Nodup ∧ ∀ r ∈ terminals34, r.source = state34 := by decide

theorem row34_sound : ∀ e ∈ edges34,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row34_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state34.started = false → 0 < q.val) → (q.val + b.val) / 10 = state34.high →
    (⟨state34, q.val, emit state34 q.val b.val, nextState state34 q.val b.val⟩ : Edge) ∈ edges34 := by decide

theorem terminal_row34_sound : ∀ r ∈ terminals34,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row34_complete : ∀ c ∈ centers, Terminal state34 c →
    (⟨state34, c, terminalExtra state34 c, terminalCenter state34 c⟩ : TerminalRow) ∈ terminals34 := by decide

theorem row35_separated : edges35.Nodup ∧ ∀ e ∈ edges35, e.source = state35 := by decide
theorem terminal_row35_separated : terminals35.Nodup ∧ ∀ r ∈ terminals35, r.source = state35 := by decide

theorem row35_sound : ∀ e ∈ edges35,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row35_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state35.started = false → 0 < q.val) → (q.val + b.val) / 10 = state35.high →
    (⟨state35, q.val, emit state35 q.val b.val, nextState state35 q.val b.val⟩ : Edge) ∈ edges35 := by decide

theorem terminal_row35_sound : ∀ r ∈ terminals35,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row35_complete : ∀ c ∈ centers, Terminal state35 c →
    (⟨state35, c, terminalExtra state35 c, terminalCenter state35 c⟩ : TerminalRow) ∈ terminals35 := by decide

theorem row36_separated : edges36.Nodup ∧ ∀ e ∈ edges36, e.source = state36 := by decide
theorem terminal_row36_separated : terminals36.Nodup ∧ ∀ r ∈ terminals36, r.source = state36 := by decide

theorem row36_sound : ∀ e ∈ edges36,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row36_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state36.started = false → 0 < q.val) → (q.val + b.val) / 10 = state36.high →
    (⟨state36, q.val, emit state36 q.val b.val, nextState state36 q.val b.val⟩ : Edge) ∈ edges36 := by decide

theorem terminal_row36_sound : ∀ r ∈ terminals36,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row36_complete : ∀ c ∈ centers, Terminal state36 c →
    (⟨state36, c, terminalExtra state36 c, terminalCenter state36 c⟩ : TerminalRow) ∈ terminals36 := by decide

theorem row37_separated : edges37.Nodup ∧ ∀ e ∈ edges37, e.source = state37 := by decide
theorem terminal_row37_separated : terminals37.Nodup ∧ ∀ r ∈ terminals37, r.source = state37 := by decide

theorem row37_sound : ∀ e ∈ edges37,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row37_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state37.started = false → 0 < q.val) → (q.val + b.val) / 10 = state37.high →
    (⟨state37, q.val, emit state37 q.val b.val, nextState state37 q.val b.val⟩ : Edge) ∈ edges37 := by decide

theorem terminal_row37_sound : ∀ r ∈ terminals37,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row37_complete : ∀ c ∈ centers, Terminal state37 c →
    (⟨state37, c, terminalExtra state37 c, terminalCenter state37 c⟩ : TerminalRow) ∈ terminals37 := by decide

theorem row38_separated : edges38.Nodup ∧ ∀ e ∈ edges38, e.source = state38 := by decide
theorem terminal_row38_separated : terminals38.Nodup ∧ ∀ r ∈ terminals38, r.source = state38 := by decide

theorem row38_sound : ∀ e ∈ edges38,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row38_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state38.started = false → 0 < q.val) → (q.val + b.val) / 10 = state38.high →
    (⟨state38, q.val, emit state38 q.val b.val, nextState state38 q.val b.val⟩ : Edge) ∈ edges38 := by decide

theorem terminal_row38_sound : ∀ r ∈ terminals38,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row38_complete : ∀ c ∈ centers, Terminal state38 c →
    (⟨state38, c, terminalExtra state38 c, terminalCenter state38 c⟩ : TerminalRow) ∈ terminals38 := by decide

theorem row39_separated : edges39.Nodup ∧ ∀ e ∈ edges39, e.source = state39 := by decide
theorem terminal_row39_separated : terminals39.Nodup ∧ ∀ r ∈ terminals39, r.source = state39 := by decide

theorem row39_sound : ∀ e ∈ edges39,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row39_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state39.started = false → 0 < q.val) → (q.val + b.val) / 10 = state39.high →
    (⟨state39, q.val, emit state39 q.val b.val, nextState state39 q.val b.val⟩ : Edge) ∈ edges39 := by decide

theorem terminal_row39_sound : ∀ r ∈ terminals39,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row39_complete : ∀ c ∈ centers, Terminal state39 c →
    (⟨state39, c, terminalExtra state39 c, terminalCenter state39 c⟩ : TerminalRow) ∈ terminals39 := by decide

theorem row40_separated : edges40.Nodup ∧ ∀ e ∈ edges40, e.source = state40 := by decide
theorem terminal_row40_separated : terminals40.Nodup ∧ ∀ r ∈ terminals40, r.source = state40 := by decide

theorem row40_sound : ∀ e ∈ edges40,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row40_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state40.started = false → 0 < q.val) → (q.val + b.val) / 10 = state40.high →
    (⟨state40, q.val, emit state40 q.val b.val, nextState state40 q.val b.val⟩ : Edge) ∈ edges40 := by decide

theorem terminal_row40_sound : ∀ r ∈ terminals40,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row40_complete : ∀ c ∈ centers, Terminal state40 c →
    (⟨state40, c, terminalExtra state40 c, terminalCenter state40 c⟩ : TerminalRow) ∈ terminals40 := by decide

theorem row41_separated : edges41.Nodup ∧ ∀ e ∈ edges41, e.source = state41 := by decide
theorem terminal_row41_separated : terminals41.Nodup ∧ ∀ r ∈ terminals41, r.source = state41 := by decide

theorem row41_sound : ∀ e ∈ edges41,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row41_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state41.started = false → 0 < q.val) → (q.val + b.val) / 10 = state41.high →
    (⟨state41, q.val, emit state41 q.val b.val, nextState state41 q.val b.val⟩ : Edge) ∈ edges41 := by decide

theorem terminal_row41_sound : ∀ r ∈ terminals41,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row41_complete : ∀ c ∈ centers, Terminal state41 c →
    (⟨state41, c, terminalExtra state41 c, terminalCenter state41 c⟩ : TerminalRow) ∈ terminals41 := by decide

theorem row42_separated : edges42.Nodup ∧ ∀ e ∈ edges42, e.source = state42 := by decide
theorem terminal_row42_separated : terminals42.Nodup ∧ ∀ r ∈ terminals42, r.source = state42 := by decide

theorem row42_sound : ∀ e ∈ edges42,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row42_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state42.started = false → 0 < q.val) → (q.val + b.val) / 10 = state42.high →
    (⟨state42, q.val, emit state42 q.val b.val, nextState state42 q.val b.val⟩ : Edge) ∈ edges42 := by decide

theorem terminal_row42_sound : ∀ r ∈ terminals42,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row42_complete : ∀ c ∈ centers, Terminal state42 c →
    (⟨state42, c, terminalExtra state42 c, terminalCenter state42 c⟩ : TerminalRow) ∈ terminals42 := by decide

theorem row43_separated : edges43.Nodup ∧ ∀ e ∈ edges43, e.source = state43 := by decide
theorem terminal_row43_separated : terminals43.Nodup ∧ ∀ r ∈ terminals43, r.source = state43 := by decide

theorem row43_sound : ∀ e ∈ edges43,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row43_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state43.started = false → 0 < q.val) → (q.val + b.val) / 10 = state43.high →
    (⟨state43, q.val, emit state43 q.val b.val, nextState state43 q.val b.val⟩ : Edge) ∈ edges43 := by decide

theorem terminal_row43_sound : ∀ r ∈ terminals43,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row43_complete : ∀ c ∈ centers, Terminal state43 c →
    (⟨state43, c, terminalExtra state43 c, terminalCenter state43 c⟩ : TerminalRow) ∈ terminals43 := by decide

theorem row44_separated : edges44.Nodup ∧ ∀ e ∈ edges44, e.source = state44 := by decide
theorem terminal_row44_separated : terminals44.Nodup ∧ ∀ r ∈ terminals44, r.source = state44 := by decide

theorem row44_sound : ∀ e ∈ edges44,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row44_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state44.started = false → 0 < q.val) → (q.val + b.val) / 10 = state44.high →
    (⟨state44, q.val, emit state44 q.val b.val, nextState state44 q.val b.val⟩ : Edge) ∈ edges44 := by decide

theorem terminal_row44_sound : ∀ r ∈ terminals44,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row44_complete : ∀ c ∈ centers, Terminal state44 c →
    (⟨state44, c, terminalExtra state44 c, terminalCenter state44 c⟩ : TerminalRow) ∈ terminals44 := by decide

theorem row45_separated : edges45.Nodup ∧ ∀ e ∈ edges45, e.source = state45 := by decide
theorem terminal_row45_separated : terminals45.Nodup ∧ ∀ r ∈ terminals45, r.source = state45 := by decide

theorem row45_sound : ∀ e ∈ edges45,
    e.source ∈ states ∧ e.target ∈ states ∧
    Transition e.source e.input e.target ∧ e.output = emit e.source e.input e.target.high := by decide

theorem row45_complete : ∀ (q : Fin 19) (b : Fin 2),
    (state45.started = false → 0 < q.val) → (q.val + b.val) / 10 = state45.high →
    (⟨state45, q.val, emit state45 q.val b.val, nextState state45 q.val b.val⟩ : Edge) ∈ edges45 := by decide

theorem terminal_row45_sound : ∀ r ∈ terminals45,
    r.source ∈ states ∧ Terminal r.source r.center ∧
    r.extra = terminalExtra r.source r.center ∧ r.outputCenter = terminalCenter r.source r.center := by decide

theorem terminal_row45_complete : ∀ c ∈ centers, Terminal state45 c →
    (⟨state45, c, terminalExtra state45 c, terminalCenter state45 c⟩ : TerminalRow) ∈ terminals45 := by decide

end Agent107.FoldedTransducer.Table
