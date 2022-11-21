#!/usr/bin/python

import sys, random
import rstr
from subprocess import Popen, PIPE


CHALLENGE_NAME = "koderod"


def flag_func(cur, nxt, dummies):
	rnd = random.randint(0,255)
	cases = ["case {1}: return func_{0}(); break;".format(nxt, rnd)]
	
	rnds = [rnd]
	for _ in range(9):
		rnd = random.randint(0,255)
		while rnd in rnds:
			rnd = random.randint(0,255)
		rnds.append(rnd)
		cases.append("case {1}: return func_{0}(); break;".format(random.choice(dummies), rnd))

	random.shuffle(cases)

	return cur, """int func_{0}();
		""".format(cur), """int func_{0}()
		{{
			uint8_t rnd;
		
			getrandom(&rnd, 1, GRND_NONBLOCK);
		
			switch (rnd)
			{{
				{1}
				default:  return func_start();
			}}
		}}

		""".format(cur, "\n".join(cases))

def gen(flag):
	replace = []
	funcs = []
	while len(flag) > 0:
		if len(flag) <= 4:
			cur = flag
			flag = ""
		else:
			cur = flag[-1]
			flag = flag[:-1]
	
		orig = cur
		
		cur = cur.replace('{', '')
		cur = cur.replace('}', '')
		cur = cur.replace('-', '')
		
		while (cur in funcs) or (cur == ''):
			cur = flag[-1] + orig
			flag = flag[:-1]
		
			orig = cur
		
			cur = cur.replace('{', '')
			cur = cur.replace('}', '')
			cur = cur.replace('-', '')
	
		replace += ["--redefine-sym", "func_" + cur + "=" + orig]

		funcs.append(cur)

	dummies = ["start"]
	replace += ["--redefine-sym", "func_start=start"]

	while len(dummies) < len(funcs) * 10:
		tmp = rstr.xeger('[a-zA-Z0-9]{{{0}}}'.format(random.randint(1,3)))

		if tmp not in funcs and tmp not in dummies:
			dummies.append(tmp)
			replace += ["--redefine-sym", "func_" + tmp + "=" + tmp]

	declarations = []
	definitions = []

	nxt = "end"
	replace += ["--redefine-sym", "func_end=end"]
	for cur in funcs:
		nxt, df, func = flag_func(cur, nxt, dummies)
		declarations.append(df)
		definitions.append(func)

	for cur in dummies:
		nxt, df, func = flag_func(cur, random.choice(dummies), dummies)
		declarations.append(df)
		definitions.append(func)
	
	random.shuffle(definitions)
	
	code = """#include <stdio.h>
	#include <stdint.h>
	#include <sys/random.h>

	int func_end()
	{{
		return 0;
	}}

	{0}
 
	int main()
	{{
		return func_start();
	}}
	""".format("\n".join(declarations) + "\n".join(definitions))
	p1 = Popen(['gcc', '-gdwarf-4', '-o', CHALLENGE_NAME, '-no-pie', '-x', 'c', '-'], stdin=PIPE)
	p1.communicate(code.encode('utf-8'))
	p2 = Popen(['objcopy'] + replace + [CHALLENGE_NAME, CHALLENGE_NAME])
	p2.communicate()


if __name__ == "__main__":
	if len(sys.argv) > 1:
		flag = sys.argv[1].strip()
	else:
		flag = sys.stdin.readline().strip()

	print("Flag: " + flag)
	
	gen(flag)

	print(f"Generated executable '{CHALLENGE_NAME}'.")
