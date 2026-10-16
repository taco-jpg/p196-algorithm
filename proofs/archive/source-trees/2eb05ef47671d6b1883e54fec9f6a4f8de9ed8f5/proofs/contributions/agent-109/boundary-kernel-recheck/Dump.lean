import BoundaryDataK
open Sofic BoundaryCertificate
def dumpNodes (g : Graph) : String :=
  String.intercalate ";" ((rawNodes fiber g).map fun (e, x) => s!"{e.src},{e.dst},{e.lab},{x}")
def dumpEdges (g : Graph) : String :=
  String.intercalate ";" (g.map fun e => s!"{e.src},{e.dst},{e.lab}")
def dumpArr (a : Array Nat) : String := String.intercalate "," (a.toList.map toString)
#eval IO.println ("G0|" ++ dumpEdges graph0K ++ "|" ++ dumpNodes graph0K ++ "|" ++ dumpArr ranks0K ++ "|" ++ dumpArr maps0K)
#eval IO.println ("G1|" ++ dumpEdges graph1K ++ "|" ++ dumpNodes graph1K ++ "|" ++ dumpArr ranks1K ++ "|" ++ dumpArr maps1K)
#eval IO.println ("G2|" ++ dumpEdges graph2K ++ "|" ++ dumpNodes graph2K ++ "|" ++ dumpArr ranks2K ++ "|" ++ dumpArr maps2K)
#eval IO.println ("G3|" ++ dumpEdges graph3K ++ "|" ++ dumpNodes graph3K ++ "|" ++ dumpArr ranks3K ++ "|" ++ dumpArr maps3K)
#eval IO.println ("G4|" ++ dumpEdges graph4K ++ "|" ++ dumpNodes graph4K ++ "|" ++ dumpArr ranks4K ++ "|" ++ dumpArr maps4K)
#eval IO.println ("G5|" ++ dumpEdges graph5K ++ "|" ++ dumpNodes graph5K ++ "|" ++ dumpArr ranks5K ++ "|" ++ dumpArr maps5K)
#eval IO.println ("G6|" ++ dumpEdges graph6K ++ "|" ++ dumpNodes graph6K ++ "|" ++ dumpArr ranks6K ++ "|" ++ dumpArr maps6K)
#eval IO.println ("G7|" ++ dumpEdges graph7K ++ "|" ++ dumpNodes graph7K ++ "|" ++ dumpArr ranks7K ++ "|" ++ dumpArr maps7K)
