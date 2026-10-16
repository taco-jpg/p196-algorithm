"""Independent ordinary-integer controls; reproducible and dependency-free."""
import json
import random
import unittest
from quotient import State, PHASES, integer_control, states, step

class TestQuotient(unittest.TestCase):
    def test_empty_interfaces_all_phases(self):
        for c in range(1,18):
            if c == 9:
                continue
            for g in range(2,6):
                for h in range(2,6):
                    integer_control(State(c), g, h)

    def test_all_small_interfaces(self):
        for s in states(3):
            s.validate(trimmed=True)
            for g,h in ((2,2),(2,3),(3,2),(4,5)):
                integer_control(s,g,h)

    def test_untrimmed_random_interfaces(self):
        r = random.Random(1964001)
        for _ in range(10000):
            c = r.choice(tuple(x for x in range(1,18) if x != 9))
            B = tuple(r.randrange(19) for _ in range(r.randrange(7)))
            if B and not B[0]:
                B = (r.randrange(1,19),) + B[1:]
            A = tuple(r.randrange(19) for _ in range(r.randrange(7)))
            half = tuple(r.randrange(19) for _ in range(r.randrange(6)))
            C = half + (() if r.randrange(2) else (2*r.randrange(10),)) + half[::-1]
            integer_control(State(c,B,A,C), r.randrange(2,8), r.randrange(2,8))

    def test_interface_enumeration_unique(self):
        for cap in range(5):
            ss = list(states(cap))
            self.assertEqual(len(ss),len(set(ss)))
            self.assertTrue(all(s.interface_size<=cap for s in ss))

if __name__ == '__main__':
    unittest.main(verbosity=2)
