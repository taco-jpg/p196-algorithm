import inspect
import outer_invariant_cadical as engine
from novel_encoding_phase24_boundary import build
source=inspect.getsource(engine.run_solver).replace("'solve-eqs',",'').replace("'elim-uncnstr',",'')
env=dict(vars(engine));exec(source,env)
s,e=build((2,8,8),16)
env['run_solver'](s,e,'novel_encoding_phase24_288_K16',30)
