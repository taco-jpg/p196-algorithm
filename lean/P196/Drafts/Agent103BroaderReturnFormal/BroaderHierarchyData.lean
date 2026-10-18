import P196.Drafts.Agent103BroaderReturnFormal.BJobData0
import P196.Drafts.Agent103BroaderReturnFormal.BJobData1
import P196.Drafts.Agent103BroaderReturnFormal.BJobData2
import P196.Drafts.Agent103BroaderReturnFormal.BJobData3
import P196.Drafts.Agent103BroaderReturnFormal.BJobData4
import P196.Drafts.Agent103BroaderReturnFormal.BJobData5
import P196.Drafts.Agent103BroaderReturnFormal.BJobData6
import P196.Drafts.Agent103BroaderReturnFormal.BJobData7
import P196.Drafts.Agent103BroaderReturnFormal.BJobData8
import P196.Drafts.Agent103BroaderReturnFormal.BJobData9
import P196.Drafts.Agent103BroaderReturnFormal.BJobData10
import P196.Drafts.Agent103BroaderReturnFormal.BJobData11
import P196.Drafts.Agent103BroaderReturnFormal.BJobData12
import P196.Drafts.Agent103BroaderReturnFormal.BJobData13
import P196.Drafts.Agent103BroaderReturnFormal.BJobData14
import P196.Drafts.D20261015ScalarHierarchyReviewSourceSnapshots.ActualJobFamily

namespace BroaderHierarchy
open ScalarFinite BroaderJobData ActualPrefixLift
set_option maxHeartbeats 0

inductive Job where
  | j0
  | j1
  | j2
  | j3
  | j4
  | j5
  | j6
  | j7
  | j8
  | j9
  | j10
  | j11
  | j12
  | j13
  | j14
  deriving DecidableEq

def data : Job → Data
  | .j0 => data0
  | .j1 => data1
  | .j2 => data2
  | .j3 => data3
  | .j4 => data4
  | .j5 => data5
  | .j6 => data6
  | .j7 => data7
  | .j8 => data8
  | .j9 => data9
  | .j10 => data10
  | .j11 => data11
  | .j12 => data12
  | .j13 => data13
  | .j14 => data14

def ranking : Job → Ranking
  | .j0 => ranking0
  | .j1 => ranking1
  | .j2 => ranking2
  | .j3 => ranking3
  | .j4 => ranking4
  | .j5 => ranking5
  | .j6 => ranking6
  | .j7 => ranking7
  | .j8 => ranking8
  | .j9 => ranking9
  | .j10 => ranking10
  | .j11 => ranking11
  | .j12 => ranking12
  | .j13 => ranking13
  | .j14 => ranking14

def width : Job → Nat
  | .j0 => jobWidth 0
  | .j1 => jobWidth 1
  | .j2 => jobWidth 2
  | .j3 => jobWidth 3
  | .j4 => jobWidth 4
  | .j5 => jobWidth 5
  | .j6 => jobWidth 6
  | .j7 => jobWidth 7
  | .j8 => jobWidth 8
  | .j9 => jobWidth 9
  | .j10 => jobWidth 10
  | .j11 => jobWidth 11
  | .j12 => jobWidth 12
  | .j13 => jobWidth 13
  | .j14 => jobWidth 14

def bound : Job → Nat
  | .j0 => jobBound 0
  | .j1 => jobBound 1
  | .j2 => jobBound 2
  | .j3 => jobBound 3
  | .j4 => jobBound 4
  | .j5 => jobBound 5
  | .j6 => jobBound 6
  | .j7 => jobBound 7
  | .j8 => jobBound 8
  | .j9 => jobBound 9
  | .j10 => jobBound 10
  | .j11 => jobBound 11
  | .j12 => jobBound 12
  | .j13 => jobBound 13
  | .j14 => jobBound 14

def child : Job → Nat → Job
  | .j0, c => if c=0 then .j1 else .j0
  | .j1, c => if c=153 then .j2 else if c=180 then .j3 else .j0
  | .j2, c => .j0
  | .j3, c => if c=117 then .j4 else .j0
  | .j4, c => if c=459 then .j5 else .j0
  | .j5, c => if c=3079 then .j6 else .j0
  | .j6, c => if c=5241 then .j7 else .j0
  | .j7, c => if c=9643 then .j8 else .j0
  | .j8, c => if c=10716 then .j9 else .j0
  | .j9, c => if c=860 then .j10 else .j0
  | .j10, c => if c=3350 then .j11 else if c=4628 then .j14 else .j0
  | .j11, c => if c=3239 then .j12 else .j0
  | .j12, c => if c=10589 then .j13 else .j0
  | .j13, c => .j0
  | .j14, c => .j0

def graph (j : Job) := ScalarFinite.graph (data j)
def component (j : Job) := (ranking j).component
def cyclic (j : Job) := (ranking j).cyclic
def rank (j : Job) := (ranking j).rank
def height (j : Job) := 14-width j

theorem weight_eq (j : Job) (c : Nat) :
    ComponentHierarchy.jobWeight cyclic child bound j c = (ranking j).weight c := by
  cases j
  · by_cases h0 : c=0
    · subst c
      decide
    · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking0, childCode0, child, h0]
  · by_cases h0 : c=153
    · subst c
      decide
    · by_cases h1 : c=180
      · subst c
        decide
      · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking1, childCode1, child, h0, h1]
  · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking2, childCode2, child]
  · by_cases h0 : c=117
    · subst c
      decide
    · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking3, childCode3, child, h0]
  · by_cases h0 : c=459
    · subst c
      decide
    · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking4, childCode4, child, h0]
  · by_cases h0 : c=3079
    · subst c
      decide
    · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking5, childCode5, child, h0]
  · by_cases h0 : c=5241
    · subst c
      decide
    · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking6, childCode6, child, h0]
  · by_cases h0 : c=9643
    · subst c
      decide
    · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking7, childCode7, child, h0]
  · by_cases h0 : c=10716
    · subst c
      decide
    · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking8, childCode8, child, h0]
  · by_cases h0 : c=860
    · subst c
      decide
    · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking9, childCode9, child, h0]
  · by_cases h0 : c=3350
    · subst c
      decide
    · by_cases h1 : c=4628
      · subst c
        decide
      · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking10, childCode10, child, h0, h1]
  · by_cases h0 : c=3239
    · subst c
      decide
    · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking11, childCode11, child, h0]
  · by_cases h0 : c=10589
    · subst c
      decide
    · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking12, childCode12, child, h0]
  · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking13, childCode13, child]
  · simp [ComponentHierarchy.jobWeight, ComponentHierarchy.componentWeight, cyclic, ranking, ranking14, childCode14, child]

theorem height_decreases (j : Job) (c : Nat) (hc : cyclic j c=true) :
    height (child j c) < height j := by
  cases j
  · by_cases h0 : c=0
    · subst c
      decide
    · simp [cyclic, ranking, ranking0, childCode0, h0] at hc
  · by_cases h0 : c=153
    · subst c
      decide
    · by_cases h1 : c=180
      · subst c
        decide
      · simp [cyclic, ranking, ranking1, childCode1, h0, h1] at hc
  · simp [cyclic, ranking, ranking2, childCode2] at hc
  · by_cases h0 : c=117
    · subst c
      decide
    · simp [cyclic, ranking, ranking3, childCode3, h0] at hc
  · by_cases h0 : c=459
    · subst c
      decide
    · simp [cyclic, ranking, ranking4, childCode4, h0] at hc
  · by_cases h0 : c=3079
    · subst c
      decide
    · simp [cyclic, ranking, ranking5, childCode5, h0] at hc
  · by_cases h0 : c=5241
    · subst c
      decide
    · simp [cyclic, ranking, ranking6, childCode6, h0] at hc
  · by_cases h0 : c=9643
    · subst c
      decide
    · simp [cyclic, ranking, ranking7, childCode7, h0] at hc
  · by_cases h0 : c=10716
    · subst c
      decide
    · simp [cyclic, ranking, ranking8, childCode8, h0] at hc
  · by_cases h0 : c=860
    · subst c
      decide
    · simp [cyclic, ranking, ranking9, childCode9, h0] at hc
  · by_cases h0 : c=3350
    · subst c
      decide
    · by_cases h1 : c=4628
      · subst c
        decide
      · simp [cyclic, ranking, ranking10, childCode10, h0, h1] at hc
  · by_cases h0 : c=3239
    · subst c
      decide
    · simp [cyclic, ranking, ranking11, childCode11, h0] at hc
  · by_cases h0 : c=10589
    · subst c
      decide
    · simp [cyclic, ranking, ranking12, childCode12, h0] at hc
  · simp [cyclic, ranking, ranking13, childCode13] at hc
  · simp [cyclic, ranking, ranking14, childCode14] at hc

theorem width_valid (L : Nat) (hL : 14 ≤ L) (j : Job) (c : Nat) (hc : cyclic j c=true) :
    1 ≤ width j ∧ width j < L ∧ width (child j c) = width j + 1 := by
  cases j
  · by_cases h0 : c=0
    · subst c
      dsimp [width, child, jobWidth, widths]
      omega
    · simp [cyclic, ranking, ranking0, childCode0, h0] at hc
  · by_cases h0 : c=153
    · subst c
      dsimp [width, child, jobWidth, widths]
      omega
    · by_cases h1 : c=180
      · subst c
        dsimp [width, child, jobWidth, widths]
        omega
      · simp [cyclic, ranking, ranking1, childCode1, h0, h1] at hc
  · simp [cyclic, ranking, ranking2, childCode2] at hc
  · by_cases h0 : c=117
    · subst c
      dsimp [width, child, jobWidth, widths]
      omega
    · simp [cyclic, ranking, ranking3, childCode3, h0] at hc
  · by_cases h0 : c=459
    · subst c
      dsimp [width, child, jobWidth, widths]
      omega
    · simp [cyclic, ranking, ranking4, childCode4, h0] at hc
  · by_cases h0 : c=3079
    · subst c
      dsimp [width, child, jobWidth, widths]
      omega
    · simp [cyclic, ranking, ranking5, childCode5, h0] at hc
  · by_cases h0 : c=5241
    · subst c
      dsimp [width, child, jobWidth, widths]
      omega
    · simp [cyclic, ranking, ranking6, childCode6, h0] at hc
  · by_cases h0 : c=9643
    · subst c
      dsimp [width, child, jobWidth, widths]
      omega
    · simp [cyclic, ranking, ranking7, childCode7, h0] at hc
  · by_cases h0 : c=10716
    · subst c
      dsimp [width, child, jobWidth, widths]
      omega
    · simp [cyclic, ranking, ranking8, childCode8, h0] at hc
  · by_cases h0 : c=860
    · subst c
      dsimp [width, child, jobWidth, widths]
      omega
    · simp [cyclic, ranking, ranking9, childCode9, h0] at hc
  · by_cases h0 : c=3350
    · subst c
      dsimp [width, child, jobWidth, widths]
      omega
    · by_cases h1 : c=4628
      · subst c
        dsimp [width, child, jobWidth, widths]
        omega
      · simp [cyclic, ranking, ranking10, childCode10, h0, h1] at hc
  · by_cases h0 : c=3239
    · subst c
      dsimp [width, child, jobWidth, widths]
      omega
    · simp [cyclic, ranking, ranking11, childCode11, h0] at hc
  · by_cases h0 : c=10589
    · subst c
      dsimp [width, child, jobWidth, widths]
      omega
    · simp [cyclic, ranking, ranking12, childCode12, h0] at hc
  · simp [cyclic, ranking, ranking13, childCode13] at hc
  · simp [cyclic, ranking, ranking14, childCode14] at hc

theorem bound_eq (j : Job) : (ranking j).bound = bound j := by
  cases j <;> rfl

end BroaderHierarchy
