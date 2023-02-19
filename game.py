import pyxel
import random


PUZZLE_HEIGHT = 4
PUZZLE_WIDTH = 4
PUZZLE_MARGIN_TOP = 90
PUZZLE_MARGIN_LEFT = 50

RULES = ["Star", "Stop", "Straight", "Curve", "Side1", "Side2", "Side3", "UpArrow1", "UpArrow2", "UpArrow3", 
		"RightArrow1", "RightArrow2", "RightArrow3", "DownArrow1", "DownArrow2", "DownArrow3", "LeftArrow1", "LeftArrow2", "LeftArrow3"]
RULE_VALID_POS = {}

NORMAL_RULE_SCORE = 10
NORMAL_RULE_PENALTY = 100
SUPER_RULE_SCORE = 150
SUPER_RULE_PENALTY = 200

MAX_TURN = 20

def init_rule_valid_position():
	for rule in RULES:
		RULE_VALID_POS[rule] = init_rule_valid_position_sub(rule)

def init_rule_valid_position_sub(s):
	ret = []
	if s == "Star":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if i%2 == 1 and j%2 == 1:
					continue

				else:
					ret.append((i, j))

	elif s == "Stop":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if (i%2 == 0 and j%2 == 1) or (i%2 == 1 and j%2 == 0):
					ret.append((i, j))

	elif s == "Straight":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if i%2 == 0 and j%2 == 0 and (i, j) != (0, 0) and (i, j) != (0, 2*PUZZLE_WIDTH-2) and (i, j) != (2*PUZZLE_HEIGHT-2, 0) and (i, j) != (2*PUZZLE_HEIGHT-2, 2*PUZZLE_WIDTH-2):
					ret.append((i, j))

	elif s == "Curve":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if i%2 == 0 and j%2 == 0:
					ret.append((i, j))

	elif s == "Side1" or s == "Side2" or s == "Side3" or s == "UpArrow1" or s == "RightArrow1" or s == "DownArrow1" or s == "LeftArrow1":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if i%2 == 1 and j%2 == 1:
					ret.append((i, j))

	elif s == "UpArrow2":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if i%2 == 1 and j%2 == 1 and i > 1:
					ret.append((i, j))

	elif s == "UpArrow3":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if i%2 == 1 and j%2 == 1 and i > 3:
					ret.append((i, j))

	elif s == "RightArrow2":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if i%2 == 1 and j%2 == 1 and j < 2*PUZZLE_WIDTH-3:
					ret.append((i, j))

	elif s == "RightArrow3":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if i%2 == 1 and j%2 == 1 and j < 2*PUZZLE_WIDTH-5:
					ret.append((i, j))

	elif s == "DownArrow2":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if i%2 == 1 and j%2 == 1 and i < 2*PUZZLE_HEIGHT-3:
					ret.append((i, j))

	elif s == "DownArrow3":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if i%2 == 1 and j%2 == 1 and i < 2*PUZZLE_HEIGHT-5:
					ret.append((i, j))

	elif s == "LeftArrow2":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if i%2 == 1 and j%2 == 1 and j > 1:
					ret.append((i, j))

	elif s == "LeftArrow3":
		for i in range(2*PUZZLE_HEIGHT-1):
			for j in range(2*PUZZLE_WIDTH-1):
				if i%2 == 1 and j%2 == 1 and j > 3:
					ret.append((i, j))

	return ret

init_rule_valid_position()


class App:
	def __init__(self):
		pyxel.init(200, 280, title="Game1", display_scale=2)
		pyxel.mouse(True)

		self.phase = "TITLE"
		self.player = 1
		self.player1_score = self.player2_score = 1000
		self.score = 0
		self.turn = 1
		self.animate_frame_limit = 0
		self.start_solving_frame = 0
		self.solve_frame = 0
		self.start_pos = self.current_pos = (PUZZLE_HEIGHT-1, 0)
		# puzzle_map:
		#   0: normal
		#   1: visited
		#   2: start
		self.puzzle_map = [[0 for j in range(PUZZLE_WIDTH)] for i in range(PUZZLE_HEIGHT)]
		self.puzzle_map[self.start_pos[0]][self.start_pos[1]] = 2
		self.movement_log = []
		# rule_list: [((h, w), rule_name), ...]
		self.rule_list = []
		self.point_rule_list = []
		# rule_stack: [rule_name, ...]
		self.rule_stack = []
		self.set_rule_stack()

		self.rule_putting_valid_pos = []
		self.rule_putting_idx = 0

		self.set_initial_rule(3)

		pyxel.run(self.update, self.draw)


	def update(self):
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

		if self.phase == "TITLE":
			if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.KEY_RETURN):
				self.go_to_the_next_phase()

		elif self.phase == "SOLVE":
			if pyxel.btnp(pyxel.KEY_UP, 20, 10):
				self.move_player("UP")

			if pyxel.btnp(pyxel.KEY_RIGHT, 20, 10):
				self.move_player("RIGHT")

			if pyxel.btnp(pyxel.KEY_DOWN, 20, 10):
				self.move_player("DOWN")

			if pyxel.btnp(pyxel.KEY_LEFT, 20, 10):
				self.move_player("LEFT")

			if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.KEY_RETURN):
				self.go_to_the_next_phase()

		elif self.phase == "TURN_RESULT":
			if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.KEY_RETURN):
				self.animate_frame_limit = -1

		elif self.phase == "PUT_RULE":
			if pyxel.btnp(pyxel.KEY_RIGHT, 20, 3):
				self.rule_putting_idx = self.rule_putting_idx+1 if self.rule_putting_idx+1 <= len(self.rule_putting_valid_pos)-1 else 0

			if pyxel.btnp(pyxel.KEY_LEFT, 20, 3):
				self.rule_putting_idx = self.rule_putting_idx-1 if self.rule_putting_idx-1 >= 0 else len(self.rule_putting_valid_pos)-1

			if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.KEY_RETURN):
				self.go_to_the_next_phase()

		elif self.phase == "RESULT":
			if pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.KEY_RETURN):
				self.go_to_the_next_phase()


	def go_to_the_next_phase(self):
		if self.phase == "TITLE":
			self.start_solving_frame = pyxel.frame_count
			self.phase = "SOLVE"

		elif self.phase == "SOLVE":
			self.animate_frame_limit = pyxel.frame_count + 1800
			self.solve_frame = pyxel.frame_count - self.start_solving_frame
			self.phase = "TURN_RESULT"

		elif self.phase == "TURN_RESULT":
			if self.player == 1:
				self.player1_score += self.score
				self.player1_score = max(0, self.player1_score)

			elif self.player == 2:
				self.player2_score += self.score
				self.player2_score = max(0, self.player2_score)

			self.score = 0
			self.start_pos = self.current_pos
			self.puzzle_map = [[0 for j in range(PUZZLE_WIDTH)] for i in range(PUZZLE_HEIGHT)]
			self.puzzle_map[self.start_pos[0]][self.start_pos[1]] = 2
			self.movement_log = []
			self.rule_putting_idx = 0

			rule_used_pos = [pos for (pos, rule_name) in self.rule_list]
			c_start_pos = (2*self.start_pos[0], 2*self.start_pos[1])
			self.rule_putting_valid_pos = [pos for pos in RULE_VALID_POS[self.rule_stack[0]] if (pos not in rule_used_pos and pos != c_start_pos)]
			if self.turn < MAX_TURN:
				self.phase = "PUT_RULE"

			else:
				self.phase = "RESULT"

		elif self.phase == "PUT_RULE":
			selected_rule = self.rule_stack[0]
			del self.rule_stack[0]
			if len(self.rule_stack) == 0:
				self.set_rule_stack()
			pos = self.rule_putting_valid_pos[self.rule_putting_idx]
			self.rule_list.append((pos, selected_rule))
			self.point_rule_list.append(0)

			rule_used_pos = [pos for (pos, rule_name) in self.rule_list]
			c_start_pos = (2*self.start_pos[0], 2*self.start_pos[1])
			while True:
				self.rule_putting_valid_pos = [pos for pos in RULE_VALID_POS[self.rule_stack[0]] if (pos not in rule_used_pos and pos != c_start_pos)]
				if len(self.rule_putting_valid_pos) > 0:
					break
				del self.rule_stack[0]
				if len(self.rule_stack) == 0:
					self.set_rule_stack()

			self.player ^= 3
			self.turn += 1
			self.start_solving_frame = pyxel.frame_count
			self.phase = "SOLVE"

		elif self.phase == "RESULT":
			self.player = 1
			self.player1_score = self.player2_score = 0
			self.score = 0
			self.turn = 1
			self.start_pos = self.current_pos = (PUZZLE_HEIGHT-1, 0)
			self.puzzle_map = [[0 for j in range(PUZZLE_WIDTH)] for i in range(PUZZLE_HEIGHT)]
			self.puzzle_map[self.start_pos[0]][self.start_pos[1]] = 2
			self.movement_log = []
			self.rule_list = []
			self.point_rule_list = []
			self.rule_stack = []
			self.rule_putting_valid_pos = []
			self.rule_putting_idx = 0
			self.set_rule_stack()
			self.set_initial_rule(3)
			self.phase = "SOLVE"


	def set_initial_rule(self, n):
		'''
		self.rule_list.append(((1, 1), "RightArrow2"))
		self.rule_list.append(((3, 5), "Side2"))
		self.rule_list.append(((6, 3), "Star"))
		self.point_rule_list.append(0)
		self.point_rule_list.append(0)
		self.point_rule_list.append(0)
		'''
		used_rule = []
		rule_used_pos = []
		cnt = 1
		count_point = count_side = count_Arrow = 0
		while True:
			selected_rule = random.choice(RULES)
			rule_pos = random.choice(RULE_VALID_POS[selected_rule])
			count_point += 1 if 0 <= RULES.index(selected_rule) <= 3 else 0
			count_side += 1 if 4 <= RULES.index(selected_rule) <= 6 else 0
			count_Arrow += 1 if 7 <= RULES.index(selected_rule) <= 18 else 0
			if rule_pos == self.start_pos or rule_pos in rule_used_pos or max(count_point, count_side, count_Arrow) >= 2:
				count_point -= 1 if 0 <= RULES.index(selected_rule) <= 3 else 0
				count_side -= 1 if 4 <= RULES.index(selected_rule) <= 6 else 0
				count_Arrow -= 1 if 7 <= RULES.index(selected_rule) <= 18 else 0
				continue
			self.rule_list.append((rule_pos, selected_rule))
			self.point_rule_list.append(0)
			used_rule.append(selected_rule)
			rule_used_pos.append(rule_pos)
			if cnt >= n:
				break
			cnt += 1


	def set_rule_stack(self):
		cnt = 1
		count_point = count_side = count_Arrow = 0
		while True:
			selected_rule = random.choice(RULES)
			count_point += 1 if 0 <= RULES.index(selected_rule) <= 3 else 0
			count_side += 1 if 4 <= RULES.index(selected_rule) <= 6 else 0
			count_Arrow += 1 if 7 <= RULES.index(selected_rule) <= 18 else 0
			if selected_rule in self.rule_stack or max(count_point, count_side, count_Arrow) >= 3:
				count_point -= 1 if 0 <= RULES.index(selected_rule) <= 3 else 0
				count_side -= 1 if 4 <= RULES.index(selected_rule) <= 6 else 0
				count_Arrow -= 1 if 7 <= RULES.index(selected_rule) <= 18 else 0
				continue
			self.rule_stack.append(selected_rule)
			if cnt >= 5:
				break
			cnt += 1


	def move_player(self, direction):
		check = self.check_movement(direction)
		if check == "NG":
			return

		cur_h, cur_w = self.current_pos
		if check == "OK":
			if direction == "UP":
				self.puzzle_map[cur_h-1][cur_w] = 1
				self.current_pos = (cur_h-1, cur_w)
				self.movement_log.append("UP")

			elif direction == "RIGHT":
				self.puzzle_map[cur_h][cur_w+1] = 1
				self.current_pos = (cur_h, cur_w+1)
				self.movement_log.append("RIGHT")

			elif direction == "DOWN":
				self.puzzle_map[cur_h+1][cur_w] = 1
				self.current_pos = (cur_h+1, cur_w)
				self.movement_log.append("DOWN")

			elif direction == "LEFT":
				self.puzzle_map[cur_h][cur_w-1] = 1
				self.current_pos = (cur_h, cur_w-1)
				self.movement_log.append("LEFT")

		elif check == "BACK":
			self.puzzle_map[cur_h][cur_w] = 0
			if direction == "UP":
				self.current_pos = (cur_h-1, cur_w)

			elif direction == "RIGHT":
				self.current_pos = (cur_h, cur_w+1)

			elif direction == "DOWN":
				self.current_pos = (cur_h+1, cur_w)

			elif direction == "LEFT":
				self.current_pos = (cur_h, cur_w-1)


	def check_movement(self, direction):
		cur_h, cur_w = self.current_pos
		if direction == "UP":
			if cur_h-1 < 0:
				return "NG"

			if self.movement_log and self.movement_log[-1] == "DOWN":
				self.movement_log.pop()
				return "BACK"

			elif self.puzzle_map[cur_h-1][cur_w]:
				return "NG"

		elif direction == "RIGHT":
			if cur_w+1 >= PUZZLE_WIDTH:
				return "NG"

			if self.movement_log and self.movement_log[-1] == "LEFT":
				self.movement_log.pop()
				return "BACK"

			elif self.puzzle_map[cur_h][cur_w+1]:
				return "NG"

		elif direction == "DOWN":
			if cur_h+1 >= PUZZLE_HEIGHT:
				return "NG"

			if self.movement_log and self.movement_log[-1] == "UP":
				self.movement_log.pop()
				return "BACK"

			elif self.puzzle_map[cur_h+1][cur_w]:
				return "NG"

		elif direction == "LEFT":
			if cur_w-1 < 0:
				return "NG"

			if self.movement_log and self.movement_log[-1] == "RIGHT":
				self.movement_log.pop()
				return "BACK"

			elif self.puzzle_map[cur_h][cur_w-1]:
				return "NG"

		return "OK"


	def judge(self):
		cur_h, cur_w = self.start_pos
		cur_h, cur_w = 2*cur_h, 2*cur_w
		locus_map = [[0 for j in range(2*PUZZLE_WIDTH-1)] for i in range(2*PUZZLE_HEIGHT-1)]
		locus_map[cur_h][cur_w] = 1
		for direction in self.movement_log:
			if direction == "UP":
				locus_map[cur_h-1][cur_w] = locus_map[cur_h-2][cur_w] = 1
				cur_h -= 2

			elif direction == "RIGHT":
				locus_map[cur_h][cur_w+1] = locus_map[cur_h][cur_w+2] = 1
				cur_w += 2

			elif direction == "DOWN":
				locus_map[cur_h+1][cur_w] = locus_map[cur_h+2][cur_w] = 1
				cur_h += 2

			elif direction == "LEFT":
				locus_map[cur_h][cur_w-1] = locus_map[cur_h][cur_w-2] = 1
				cur_w -= 2

		rule_state_list = []
		for rule in self.rule_list:
			(h, w), rule_name = rule
			if rule_name == "Star":
				rule_state_list.append(locus_map[h][w])

			elif rule_name == "Stop":
				rule_state_list.append(1^locus_map[h][w])

			elif rule_name == "Straight":
				if ((h-1 >= 0 and w-1 >= 0 and locus_map[h-1][w]&locus_map[h][w-1]) or 
					(h-1 >= 0 and w+1 < 2*PUZZLE_WIDTH-1 and locus_map[h-1][w]&locus_map[h][w+1]) or 
					(h+1 < 2*PUZZLE_HEIGHT-1 and w-1 >= 0 and locus_map[h+1][w]&locus_map[h][w-1]) or 
					(h+1 < 2*PUZZLE_HEIGHT-1 and w+1 < 2*PUZZLE_WIDTH-1 and locus_map[h+1][w]&locus_map[h][w+1])):

					rule_state_list.append(0)

				elif ((h-1 >= 0 and h+1 < 2*PUZZLE_HEIGHT-1 and locus_map[h-1][w]&locus_map[h+1][w]) or 
					(w-1 >= 0 and w+1 < 2*PUZZLE_WIDTH-1 and locus_map[h][w-1]&locus_map[h][w+1])):

					rule_state_list.append(1)

				else:
					rule_state_list.append(2)

			elif rule_name == "Curve":
				if ((h-1 >= 0 and w-1 >= 0 and locus_map[h-1][w]&locus_map[h][w-1]) or 
					(h-1 >= 0 and w+1 < 2*PUZZLE_WIDTH-1 and locus_map[h-1][w]&locus_map[h][w+1]) or 
					(h+1 < 2*PUZZLE_HEIGHT-1 and w-1 >= 0 and locus_map[h+1][w]&locus_map[h][w-1]) or 
					(h+1 < 2*PUZZLE_HEIGHT-1 and w+1 < 2*PUZZLE_WIDTH-1 and locus_map[h+1][w]&locus_map[h][w+1])):

					rule_state_list.append(1)

				elif ((h-1 >= 0 and h+1 < 2*PUZZLE_HEIGHT-1 and locus_map[h-1][w]&locus_map[h+1][w]) or 
					(w-1 >= 0 and w+1 < 2*PUZZLE_WIDTH-1 and locus_map[h][w-1]&locus_map[h][w+1])):

					rule_state_list.append(0)

				else:
					rule_state_list.append(2)

			elif "Side" in rule_name:
				count_side = locus_map[h-1][w]+locus_map[h+1][w]+locus_map[h][w-1]+locus_map[h][w+1]
				rule_state_list.append(count_side)

			elif "UpArrow" in rule_name:
				count_cross = sum([locus_map[i][w] for i in range(0, h)])
				rule_state_list.append(count_cross)

			elif "RightArrow" in rule_name:
				count_cross = sum([locus_map[h][i] for i in range(w, 2*PUZZLE_WIDTH-1)])
				rule_state_list.append(count_cross)

			elif "DownArrow" in rule_name:
				count_cross = sum([locus_map[i][w] for i in range(h, 2*PUZZLE_HEIGHT-1)])
				rule_state_list.append(count_cross)

			elif "LeftArrow" in rule_name:
				count_cross = sum([locus_map[h][i] for i in range(0, w)])
				rule_state_list.append(count_cross)

		return rule_state_list


	def draw_header(self):
		if self.player == 1:
			pyxel.rect(5, 5, 38, 20, pyxel.COLOR_YELLOW)

		elif self.player == 2:
			pyxel.rect(155, 5, 38, 20, pyxel.COLOR_YELLOW)
		pyxel.text(10, 10, f"1P\n{self.player1_score:0>7d}", pyxel.COLOR_BLACK)
		pyxel.text(160, 10, f"2P\n{self.player2_score:0>7d}", pyxel.COLOR_BLACK)
		pyxel.text(72, 13, f"TURN   {self.turn:>2d} / {MAX_TURN:>2d}", pyxel.COLOR_BLACK)
		pyxel.line(70, 21, 130, 21, pyxel.COLOR_BLACK)


	def draw_puzzle(self, idx=-1):
		visited_lines = []
		cur_h, cur_w = self.start_pos
		for direction in self.movement_log:
			if direction == "UP":
				visited_lines.append((cur_h-1, cur_w, "DOWN"))
				cur_h -= 1

			elif direction == "RIGHT":
				visited_lines.append((cur_h, cur_w, "RIGHT"))
				cur_w += 1

			elif direction == "DOWN":
				visited_lines.append((cur_h, cur_w, "DOWN"))
				cur_h += 1

			elif direction == "LEFT":
				visited_lines.append((cur_h, cur_w-1, "RIGHT"))
				cur_w -= 1

		for i in range(PUZZLE_HEIGHT):
			for j in range(PUZZLE_WIDTH):
				base_x, base_y = PUZZLE_MARGIN_LEFT+30*j, PUZZLE_MARGIN_TOP+30*i
				if i < PUZZLE_HEIGHT-1:
					if (i, j, "DOWN") in visited_lines:
						pyxel.rect(base_x+4, base_y+10, 3, 20, pyxel.COLOR_ORANGE)

					else:
						pyxel.rect(base_x+4, base_y+10, 3, 20, pyxel.COLOR_GRAY)

				if j < PUZZLE_WIDTH-1:
					if (i, j, "RIGHT") in visited_lines:
						pyxel.rect(base_x+10, base_y+4, 20, 3, pyxel.COLOR_ORANGE)

					else:
						pyxel.rect(base_x+10, base_y+4, 20, 3, pyxel.COLOR_GRAY)

				if self.puzzle_map[i][j] == 0:
					pyxel.rect(base_x, base_y, 11, 11, pyxel.COLOR_GRAY)

				elif self.puzzle_map[i][j] == 1:
					pyxel.rect(base_x, base_y, 11, 11, pyxel.COLOR_ORANGE)

				elif self.puzzle_map[i][j] == 2:
					pyxel.circ(base_x+5, base_y+5, 6, pyxel.COLOR_ORANGE)

		if idx >= 0:
			for i, pos in enumerate(self.rule_putting_valid_pos):
				(h, w) = pos
				base_x, base_y = PUZZLE_MARGIN_LEFT+30*(w/2), PUZZLE_MARGIN_TOP+30*(h/2)
				if i == idx:
					pyxel.rect(base_x+1, base_y+1, 9, 9, pyxel.COLOR_YELLOW)

				else:
					pyxel.rect(base_x+1, base_y+1, 9, 9, pyxel.COLOR_LIME)


	def draw_rule(self):
		rule_state_list = self.judge()
		for i, rule in enumerate(self.rule_list):
			effect = 3 if self.point_rule_list[i] == 1 else 0
			self.draw_one_rule(rule, rule_state_list[i], effect)


	def draw_one_rule(self, rule, state, effect):
		# effect: (0:normal, 1:red, 2:unaffected, 3:super)

		(h, w), rule_name = rule
		base_x, base_y = PUZZLE_MARGIN_LEFT+30*(w/2), PUZZLE_MARGIN_TOP+30*(h/2)
		if (h%2, w%2) == (1, 1):
			base_x -= 1

		if effect == 0:
			if rule_name == "Star":
				if state == 1:
					pyxel.circ(base_x+5, base_y+5, 4, pyxel.COLOR_YELLOW)
				pyxel.circb(base_x+5, base_y+5, 4, pyxel.COLOR_BLACK)

			elif rule_name == "Stop":
				if state == 0:
					pyxel.rect(base_x, base_y, 11, 11, pyxel.COLOR_BLACK)

				elif state == 1:
					pyxel.rect(base_x, base_y, 11, 11, pyxel.COLOR_WHITE)
				pyxel.rectb(base_x, base_y, 11, 11, pyxel.COLOR_BLACK)
				pyxel.line(base_x+2, base_y+2, base_x+8, base_y+8, pyxel.COLOR_RED)
				pyxel.line(base_x+2, base_y+8, base_x+8, base_y+2, pyxel.COLOR_RED)

			elif rule_name == "Straight":
				if state == 0:
					pyxel.circ(base_x+5, base_y+5, 5, pyxel.COLOR_BLACK)

				elif state == 1:
					pyxel.circ(base_x+5, base_y+5, 5, pyxel.COLOR_YELLOW)
				pyxel.circb(base_x+5, base_y+5, 5, pyxel.COLOR_BLACK)
				pyxel.line(base_x, base_y+5, base_x+10, base_y+5, pyxel.COLOR_BLACK)
				pyxel.line(base_x+5, base_y, base_x+5, base_y+10, pyxel.COLOR_BLACK)

			elif rule_name == "Curve":
				if state == 0:
					pyxel.circ(base_x+5, base_y+5, 5, pyxel.COLOR_BLACK)

				elif state == 1:
					pyxel.circ(base_x+5, base_y+5, 5, pyxel.COLOR_YELLOW)
				pyxel.circb(base_x+5, base_y+5, 5, pyxel.COLOR_BLACK)
				pyxel.line(base_x+2, base_y+2, base_x+8, base_y+8, pyxel.COLOR_BLACK)
				pyxel.line(base_x+2, base_y+8, base_x+8, base_y+2, pyxel.COLOR_BLACK)

			elif rule_name == "Side1":
				if state == 1:
					pyxel.rect(base_x, base_y, 13, 12, pyxel.COLOR_YELLOW)

				if state >= 2:
					pyxel.rect(base_x, base_y, 13, 12, pyxel.COLOR_BLACK)
				pyxel.rectb(base_x, base_y, 13, 12, pyxel.COLOR_BLACK)

			elif rule_name == "Side2":
				if state >= 1:
					pyxel.rect(base_x, base_y+4, 7, 8, pyxel.COLOR_YELLOW)

				if state >= 2:
					pyxel.rect(base_x+6, base_y, 7, 12, pyxel.COLOR_YELLOW)

				if state >= 3:
					pyxel.rect(base_x, base_y+4, 7, 8, pyxel.COLOR_BLACK)
					pyxel.rect(base_x+6, base_y, 7, 12, pyxel.COLOR_BLACK)
				pyxel.rectb(base_x, base_y+4, 7, 8, pyxel.COLOR_BLACK)
				pyxel.rectb(base_x+6, base_y, 7, 12, pyxel.COLOR_BLACK)

			elif rule_name == "Side3":
				if state >= 1:
					pyxel.rect(base_x, base_y+6, 5, 6, pyxel.COLOR_YELLOW)

				if state >= 2:
					pyxel.rect(base_x+4, base_y+3, 5, 9, pyxel.COLOR_YELLOW)

				if state >= 3:
					pyxel.rect(base_x+8, base_y, 5, 12, pyxel.COLOR_YELLOW)
				pyxel.rectb(base_x, base_y+6, 5, 6, pyxel.COLOR_BLACK)
				pyxel.rectb(base_x+4, base_y+3, 5, 9, pyxel.COLOR_BLACK)
				pyxel.rectb(base_x+8, base_y, 5, 12, pyxel.COLOR_BLACK)

			elif "UpArrow" in rule_name:
				num = int(rule_name[-1])-state
				if num == 0:
					pyxel.tri(base_x+2, base_y+2, base_x+10, base_y+2, base_x+6, base_y-2, pyxel.COLOR_YELLOW)
					pyxel.text(base_x+2, base_y+6, f"{num:>2d}", pyxel.COLOR_YELLOW)

				else:
					pyxel.tri(base_x+2, base_y+2, base_x+10, base_y+2, base_x+6, base_y-2, pyxel.COLOR_BLACK)
					pyxel.text(base_x+2, base_y+6, f"{num:>2d}", pyxel.COLOR_BLACK)
				pyxel.trib(base_x+2, base_y+2, base_x+10, base_y+2, base_x+6, base_y-2, pyxel.COLOR_BLACK)

			elif "RightArrow" in rule_name:
				num = int(rule_name[-1])-state
				if num == 0:
					pyxel.tri(base_x+8, base_y+1, base_x+8, base_y+9, base_x+12, base_y+5, pyxel.COLOR_YELLOW)
					pyxel.text(base_x-2, base_y+3, f"{num:>2d}", pyxel.COLOR_YELLOW)

				else:
					pyxel.tri(base_x+8, base_y+1, base_x+8, base_y+9, base_x+12, base_y+5, pyxel.COLOR_BLACK)
					pyxel.text(base_x-2, base_y+3, f"{num:>2d}", pyxel.COLOR_BLACK)
				pyxel.trib(base_x+8, base_y+1, base_x+8, base_y+9, base_x+12, base_y+5, pyxel.COLOR_BLACK)

			elif "DownArrow" in rule_name:
				num = int(rule_name[-1])-state
				if num == 0:
					pyxel.tri(base_x+2, base_y+8, base_x+10, base_y+8, base_x+6, base_y+12, pyxel.COLOR_YELLOW)
					pyxel.text(base_x+2, base_y, f"{num:>2d}", pyxel.COLOR_YELLOW)

				else:
					pyxel.tri(base_x+2, base_y+8, base_x+10, base_y+8, base_x+6, base_y+12, pyxel.COLOR_BLACK)
					pyxel.text(base_x+2, base_y, f"{num:>2d}", pyxel.COLOR_BLACK)
				pyxel.trib(base_x+2, base_y+8, base_x+10, base_y+8, base_x+6, base_y+12, pyxel.COLOR_BLACK)

			elif "LeftArrow" in rule_name:
				num = int(rule_name[-1])-state
				if num == 0:
					pyxel.tri(base_x+4, base_y+1, base_x+4, base_y+9, base_x, base_y+5, pyxel.COLOR_YELLOW)
					pyxel.text(base_x+8, base_y+3, f"{num:<2d}", pyxel.COLOR_YELLOW)

				else:
					pyxel.tri(base_x+4, base_y+1, base_x+4, base_y+9, base_x, base_y+5, pyxel.COLOR_BLACK)
					pyxel.text(base_x+8, base_y+3, f"{num:<2d}", pyxel.COLOR_BLACK)
				pyxel.trib(base_x+4, base_y+1, base_x+4, base_y+9, base_x, base_y+5, pyxel.COLOR_BLACK)

		elif effect == 1:
			if rule_name == "Star":
				pyxel.circ(base_x+5, base_y+5, 4, pyxel.COLOR_RED)

			elif rule_name == "Stop":
				pyxel.rect(base_x, base_y, 11, 11, pyxel.COLOR_RED)

			elif rule_name == "Straight":
				pyxel.circ(base_x+5, base_y+5, 5, pyxel.COLOR_RED)

			elif rule_name == "Curve":
				pyxel.circ(base_x+5, base_y+5, 5, pyxel.COLOR_RED)

			elif rule_name == "Side1":
				pyxel.rect(base_x, base_y, 13, 12, pyxel.COLOR_RED)

			elif rule_name == "Side2":
				pyxel.rect(base_x, base_y+4, 7, 8, pyxel.COLOR_RED)
				pyxel.rect(base_x+6, base_y, 7, 12, pyxel.COLOR_RED)

			elif rule_name == "Side3":
				pyxel.rect(base_x, base_y+6, 5, 6, pyxel.COLOR_RED)
				pyxel.rect(base_x+4, base_y+3, 5, 9, pyxel.COLOR_RED)
				pyxel.rect(base_x+8, base_y, 5, 12, pyxel.COLOR_RED)

			elif "UpArrow" in rule_name:
				num = int(rule_name[-1])-state
				pyxel.tri(base_x+2, base_y+2, base_x+10, base_y+2, base_x+6, base_y-2, pyxel.COLOR_RED)
				pyxel.text(base_x+2, base_y+6, f"{num:>2d}", pyxel.COLOR_RED)

			elif "RightArrow" in rule_name:
				num = int(rule_name[-1])-state
				pyxel.tri(base_x+8, base_y+1, base_x+8, base_y+9, base_x+12, base_y+5, pyxel.COLOR_RED)
				pyxel.text(base_x-2, base_y+3, f"{num:>2d}", pyxel.COLOR_RED)

			elif "DownArrow" in rule_name:
				num = int(rule_name[-1])-state
				pyxel.tri(base_x+2, base_y+8, base_x+10, base_y+8, base_x+6, base_y+12, pyxel.COLOR_RED)
				pyxel.text(base_x+2, base_y, f"{num:>2d}", pyxel.COLOR_RED)

			elif "LeftArrow" in rule_name:
				num = int(rule_name[-1])-state
				pyxel.tri(base_x+4, base_y+1, base_x+4, base_y+9, base_x, base_y+5, pyxel.COLOR_RED)
				pyxel.text(base_x+8, base_y+3, f"{num:<2d}", pyxel.COLOR_RED)

		elif effect == 2:
			if rule_name == "Star":
				pyxel.circ(base_x+5, base_y+5, 4, pyxel.COLOR_WHITE)
				pyxel.circb(base_x+5, base_y+5, 4, pyxel.COLOR_BLACK)

			elif rule_name == "Stop":
				pyxel.rect(base_x, base_y, 11, 11, pyxel.COLOR_WHITE)
				pyxel.rectb(base_x, base_y, 11, 11, pyxel.COLOR_BLACK)
				pyxel.line(base_x+2, base_y+2, base_x+8, base_y+8, pyxel.COLOR_RED)
				pyxel.line(base_x+2, base_y+8, base_x+8, base_y+2, pyxel.COLOR_RED)

			elif rule_name == "Straight":
				pyxel.circ(base_x+5, base_y+5, 5, pyxel.COLOR_WHITE)
				pyxel.circb(base_x+5, base_y+5, 5, pyxel.COLOR_BLACK)
				pyxel.line(base_x, base_y+5, base_x+10, base_y+5, pyxel.COLOR_BLACK)
				pyxel.line(base_x+5, base_y, base_x+5, base_y+10, pyxel.COLOR_BLACK)

			elif rule_name == "Curve":
				pyxel.circ(base_x+5, base_y+5, 5, pyxel.COLOR_WHITE)
				pyxel.circb(base_x+5, base_y+5, 5, pyxel.COLOR_BLACK)
				pyxel.line(base_x+2, base_y+2, base_x+8, base_y+8, pyxel.COLOR_BLACK)
				pyxel.line(base_x+2, base_y+8, base_x+8, base_y+2, pyxel.COLOR_BLACK)

			elif rule_name == "Side1":
				pyxel.rect(base_x, base_y, 13, 12, pyxel.COLOR_WHITE)
				pyxel.rectb(base_x, base_y, 13, 12, pyxel.COLOR_BLACK)

			elif rule_name == "Side2":
				pyxel.rect(base_x, base_y+4, 7, 8, pyxel.COLOR_WHITE)
				pyxel.rect(base_x+6, base_y, 7, 12, pyxel.COLOR_WHITE)
				pyxel.rectb(base_x, base_y+4, 7, 8, pyxel.COLOR_BLACK)
				pyxel.rectb(base_x+6, base_y, 7, 12, pyxel.COLOR_BLACK)

			elif rule_name == "Side3":
				pyxel.rect(base_x, base_y+6, 5, 6, pyxel.COLOR_WHITE)
				pyxel.rect(base_x+4, base_y+3, 5, 9, pyxel.COLOR_WHITE)
				pyxel.rect(base_x+8, base_y, 5, 12, pyxel.COLOR_WHITE)
				pyxel.rectb(base_x, base_y+6, 5, 6, pyxel.COLOR_BLACK)
				pyxel.rectb(base_x+4, base_y+3, 5, 9, pyxel.COLOR_BLACK)
				pyxel.rectb(base_x+8, base_y, 5, 12, pyxel.COLOR_BLACK)

			elif "UpArrow" in rule_name:
				num = int(rule_name[-1])
				pyxel.tri(base_x+2, base_y+2, base_x+10, base_y+2, base_x+6, base_y-2, pyxel.COLOR_WHITE)
				pyxel.text(base_x+2, base_y+6, f"{num:>2d}", pyxel.COLOR_BLACK)
				pyxel.trib(base_x+2, base_y+2, base_x+10, base_y+2, base_x+6, base_y-2, pyxel.COLOR_BLACK)

			elif "RightArrow" in rule_name:
				num = int(rule_name[-1])
				pyxel.tri(base_x+8, base_y+1, base_x+8, base_y+9, base_x+12, base_y+5, pyxel.COLOR_WHITE)
				pyxel.text(base_x-2, base_y+3, f"{num:>2d}", pyxel.COLOR_BLACK)
				pyxel.trib(base_x+8, base_y+1, base_x+8, base_y+9, base_x+12, base_y+5, pyxel.COLOR_BLACK)

			elif "DownArrow" in rule_name:
				num = int(rule_name[-1])
				pyxel.tri(base_x+2, base_y+8, base_x+10, base_y+8, base_x+6, base_y+12, pyxel.COLOR_WHITE)
				pyxel.text(base_x+2, base_y, f"{num:>2d}", pyxel.COLOR_BLACK)
				pyxel.trib(base_x+2, base_y+8, base_x+10, base_y+8, base_x+6, base_y+12, pyxel.COLOR_BLACK)

			elif "LeftArrow" in rule_name:
				num = int(rule_name[-1])
				pyxel.tri(base_x+4, base_y+1, base_x+4, base_y+9, base_x, base_y+5, pyxel.COLOR_WHITE)
				pyxel.text(base_x+8, base_y+3, f"{num:<2d}", pyxel.COLOR_BLACK)
				pyxel.trib(base_x+4, base_y+1, base_x+4, base_y+9, base_x, base_y+5, pyxel.COLOR_BLACK)

		elif effect == 3:
			if rule_name == "Star":
				if state == 1:
					pyxel.circ(base_x+5, base_y+5, 4, pyxel.COLOR_YELLOW)
				pyxel.circb(base_x+5, base_y+5, 4, pyxel.COLOR_GREEN)

			elif rule_name == "Stop":
				if state == 0:
					pyxel.rect(base_x, base_y, 11, 11, pyxel.COLOR_BLACK)

				elif state == 1:
					pyxel.rect(base_x, base_y, 11, 11, pyxel.COLOR_WHITE)
				pyxel.rectb(base_x, base_y, 11, 11, pyxel.COLOR_GREEN)
				pyxel.line(base_x+2, base_y+2, base_x+8, base_y+8, pyxel.COLOR_RED)
				pyxel.line(base_x+2, base_y+8, base_x+8, base_y+2, pyxel.COLOR_RED)

			elif rule_name == "Straight":
				if state == 0:
					pyxel.circ(base_x+5, base_y+5, 5, pyxel.COLOR_BLACK)

				elif state == 1:
					pyxel.circ(base_x+5, base_y+5, 5, pyxel.COLOR_YELLOW)
				pyxel.circb(base_x+5, base_y+5, 5, pyxel.COLOR_GREEN)
				pyxel.line(base_x, base_y+5, base_x+10, base_y+5, pyxel.COLOR_GREEN)
				pyxel.line(base_x+5, base_y, base_x+5, base_y+10, pyxel.COLOR_GREEN)

			elif rule_name == "Curve":
				if state == 0:
					pyxel.circ(base_x+5, base_y+5, 5, pyxel.COLOR_BLACK)

				elif state == 1:
					pyxel.circ(base_x+5, base_y+5, 5, pyxel.COLOR_YELLOW)
				pyxel.circb(base_x+5, base_y+5, 5, pyxel.COLOR_GREEN)
				pyxel.line(base_x+2, base_y+2, base_x+8, base_y+8, pyxel.COLOR_GREEN)
				pyxel.line(base_x+2, base_y+8, base_x+8, base_y+2, pyxel.COLOR_GREEN)

			elif rule_name == "Side1":
				if state == 1:
					pyxel.rect(base_x, base_y, 13, 12, pyxel.COLOR_YELLOW)

				if state >= 2:
					pyxel.rect(base_x, base_y, 13, 12, pyxel.COLOR_BLACK)
				pyxel.rectb(base_x, base_y, 13, 12, pyxel.COLOR_GREEN)

			elif rule_name == "Side2":
				if state >= 1:
					pyxel.rect(base_x, base_y+4, 7, 8, pyxel.COLOR_YELLOW)

				if state >= 2:
					pyxel.rect(base_x+6, base_y, 7, 12, pyxel.COLOR_YELLOW)

				if state >= 3:
					pyxel.rect(base_x, base_y+4, 7, 8, pyxel.COLOR_BLACK)
					pyxel.rect(base_x+6, base_y, 7, 12, pyxel.COLOR_BLACK)
				pyxel.rectb(base_x, base_y+4, 7, 8, pyxel.COLOR_GREEN)
				pyxel.rectb(base_x+6, base_y, 7, 12, pyxel.COLOR_GREEN)

			elif rule_name == "Side3":
				if state >= 1:
					pyxel.rect(base_x, base_y+6, 5, 6, pyxel.COLOR_YELLOW)

				if state >= 2:
					pyxel.rect(base_x+4, base_y+3, 5, 9, pyxel.COLOR_YELLOW)

				if state >= 3:
					pyxel.rect(base_x+8, base_y, 5, 12, pyxel.COLOR_YELLOW)
				pyxel.rectb(base_x, base_y+6, 5, 6, pyxel.COLOR_GREEN)
				pyxel.rectb(base_x+4, base_y+3, 5, 9, pyxel.COLOR_GREEN)
				pyxel.rectb(base_x+8, base_y, 5, 12, pyxel.COLOR_GREEN)

			elif "UpArrow" in rule_name:
				num = int(rule_name[-1])-state
				if num == 0:
					pyxel.tri(base_x+2, base_y+2, base_x+10, base_y+2, base_x+6, base_y-2, pyxel.COLOR_YELLOW)
					pyxel.text(base_x+2, base_y+6, f"{num:>2d}", pyxel.COLOR_YELLOW)

				else:
					pyxel.tri(base_x+2, base_y+2, base_x+10, base_y+2, base_x+6, base_y-2, pyxel.COLOR_BLACK)
					pyxel.text(base_x+2, base_y+6, f"{num:>2d}", pyxel.COLOR_GREEN)
				pyxel.trib(base_x+2, base_y+2, base_x+10, base_y+2, base_x+6, base_y-2, pyxel.COLOR_GREEN)

			elif "RightArrow" in rule_name:
				num = int(rule_name[-1])-state
				if num == 0:
					pyxel.tri(base_x+8, base_y+1, base_x+8, base_y+9, base_x+12, base_y+5, pyxel.COLOR_YELLOW)
					pyxel.text(base_x-2, base_y+3, f"{num:>2d}", pyxel.COLOR_YELLOW)

				else:
					pyxel.tri(base_x+8, base_y+1, base_x+8, base_y+9, base_x+12, base_y+5, pyxel.COLOR_BLACK)
					pyxel.text(base_x-2, base_y+3, f"{num:>2d}", pyxel.COLOR_GREEN)
				pyxel.trib(base_x+8, base_y+1, base_x+8, base_y+9, base_x+12, base_y+5, pyxel.COLOR_GREEN)

			elif "DownArrow" in rule_name:
				num = int(rule_name[-1])-state
				if num == 0:
					pyxel.tri(base_x+2, base_y+8, base_x+10, base_y+8, base_x+6, base_y+12, pyxel.COLOR_YELLOW)
					pyxel.text(base_x+2, base_y, f"{num:>2d}", pyxel.COLOR_YELLOW)

				else:
					pyxel.tri(base_x+2, base_y+8, base_x+10, base_y+8, base_x+6, base_y+12, pyxel.COLOR_BLACK)
					pyxel.text(base_x+2, base_y, f"{num:>2d}", pyxel.COLOR_GREEN)
				pyxel.trib(base_x+2, base_y+8, base_x+10, base_y+8, base_x+6, base_y+12, pyxel.COLOR_GREEN)

			elif "LeftArrow" in rule_name:
				num = int(rule_name[-1])-state
				if num == 0:
					pyxel.tri(base_x+4, base_y+1, base_x+4, base_y+9, base_x, base_y+5, pyxel.COLOR_YELLOW)
					pyxel.text(base_x+8, base_y+3, f"{num:<2d}", pyxel.COLOR_YELLOW)

				else:
					pyxel.tri(base_x+4, base_y+1, base_x+4, base_y+9, base_x, base_y+5, pyxel.COLOR_BLACK)
					pyxel.text(base_x+8, base_y+3, f"{num:<2d}", pyxel.COLOR_GREEN)
				pyxel.trib(base_x+4, base_y+1, base_x+4, base_y+9, base_x, base_y+5, pyxel.COLOR_GREEN)


	def draw_rule_stack(self, idx=-1):
		pyxel.text(PUZZLE_MARGIN_LEFT+2, 221, "NEXT PUZZLE-RULE:", pyxel.COLOR_BLACK)
		pyxel.rectb(PUZZLE_MARGIN_LEFT-4, 210, 108, 29, pyxel.COLOR_BLACK)
		pyxel.rect(PUZZLE_MARGIN_LEFT+75, 210, 29, 29, pyxel.COLOR_CYAN)
		pyxel.rectb(PUZZLE_MARGIN_LEFT+75, 210, 29, 29, pyxel.COLOR_BLACK)
		pos = (2*PUZZLE_HEIGHT+0.5, 5.5)
		rule = (pos, self.rule_stack[0])
		self.draw_one_rule(rule, 1, 2)


	def draw_turn_result(self):
		rule_state_list = self.judge()
		observed_rule_list = [] # [bool, ...]
		n_score_count = s_score_count = n_penalty_count = s_penalty_count = 0
		speed_bonus = 0
		for i, rule in enumerate(self.rule_list):
			(h, w), rule_name = rule
			if rule_name == "Star":
				if rule_state_list[i] == 1:
					observed_rule_list.append(1)

				else:
					observed_rule_list.append(0)

			elif rule_name == "Stop":
				if rule_state_list[i] == 1:
					observed_rule_list.append(1)

				else:
					observed_rule_list.append(0)

			elif rule_name == "Straight":
				if rule_state_list[i] == 1:
					observed_rule_list.append(1)

				elif rule_state_list[i] == 2 and (h, w) == (2*self.start_pos[0], 2*self.start_pos[1]):
					observed_rule_list.append(2)

				else:
					observed_rule_list.append(0)

			elif rule_name == "Curve":
				if rule_state_list[i] == 1:
					observed_rule_list.append(1)

				elif rule_state_list[i] == 2 and (h, w) == (2*self.start_pos[0], 2*self.start_pos[1]):
					observed_rule_list.append(2)

				else:
					observed_rule_list.append(0)

			elif rule_name == "Side1":
				if rule_state_list[i] == 1:
					observed_rule_list.append(1)

				else:
					observed_rule_list.append(0)

			elif rule_name == "Side2":
				if rule_state_list[i] == 2:
					observed_rule_list.append(1)

				else:
					observed_rule_list.append(0)

			elif rule_name == "Side3":
				if rule_state_list[i] == 3:
					observed_rule_list.append(1)

				else:
					observed_rule_list.append(0)

			elif "Arrow" in rule_name:
				if rule_state_list[i] == int(rule_name[-1]):
					observed_rule_list.append(1)

				else:
					observed_rule_list.append(0)

			if observed_rule_list[i] == 1:
				if self.point_rule_list[i] == 1:
					s_score_count += 1

				else:
					n_score_count += 1

			elif observed_rule_list[i] == 0:
				if self.point_rule_list[i] == 1:
					s_penalty_count += 1

				else:
					n_penalty_count += 1

		n_score = n_score_count*NORMAL_RULE_SCORE
		n_penalty = n_penalty_count*NORMAL_RULE_PENALTY
		s_score = s_score_count*SUPER_RULE_SCORE
		s_penalty = s_penalty_count*SUPER_RULE_PENALTY
		speed_bonus = int(40*len(self.rule_list) - self.solve_frame/2)
		speed_bonus = max(0, speed_bonus)
		if speed_bonus > 0:
			pyxel.text(30, 35,                f"            SPEEDY BONUS     :  +{speed_bonus}PT", pyxel.COLOR_DARK_BLUE)
		pyxel.text(30, 45, f"OBSERVED {n_score_count  :>2d} PUZZLE-RULE      :  +{n_score  }PT", pyxel.COLOR_BLACK)
		pyxel.text(30, 55, f"  BROKE  {n_penalty_count:>2d}                  :  -{n_penalty}PT", pyxel.COLOR_RED)
		pyxel.text(30, 55,                     "            PUZZLE-RULE", pyxel.COLOR_BLACK)
		pyxel.text(30, 65, f"OBSERVED {s_score_count  :>2d}                  :  +{s_score  }PT", pyxel.COLOR_BLACK)
		pyxel.text(30, 65,                     "            SUPER-PUZZLE-RULE", pyxel.COLOR_GREEN)
		pyxel.text(30, 75, f"  BROKE  {s_penalty_count:>2d}                  :  -{s_penalty}PT", pyxel.COLOR_RED)
		pyxel.text(30, 75,                     "            SUPER-PUZZLE-RULE", pyxel.COLOR_GREEN)

		for i, rule in enumerate(self.rule_list):
			effect = 3 if self.point_rule_list[i] == 1 else 0
			if observed_rule_list[i] == 0 and pyxel.frame_count%16 < 8:
				effect = 1
			self.draw_one_rule(rule, rule_state_list[i], effect)

		if pyxel.frame_count > self.animate_frame_limit:
			delete_rule_idx_list = []
			for i, is_ok in enumerate(observed_rule_list):
				if self.point_rule_list[i] == 0 and is_ok == 0:
					self.point_rule_list[i] = 1

				elif self.point_rule_list[i] == 1:
					delete_rule_idx_list.append(i)

			# 大きい順に削除しないと、idxがoverする
			for idx in reversed(delete_rule_idx_list):
				del self.rule_list[idx]
				del self.point_rule_list[idx]

			self.score += n_score + s_score - n_penalty - s_penalty + speed_bonus
			self.go_to_the_next_phase()


	def draw_result(self):
		result = "DRAW" if self.player1_score == self.player2_score else "1P WIN" if self.player1_score > self.player2_score else "2P WIN"
		pyxel.text(90, 130, result, pyxel.COLOR_BLACK)
		pyxel.text(50, 150, f"1P: {self.player1_score}PT", pyxel.COLOR_BLACK)
		pyxel.text(120, 150, f"2P: {self.player2_score}PT", pyxel.COLOR_BLACK)


	def draw(self):
		pyxel.cls(pyxel.COLOR_WHITE)
		if self.phase == "TITLE":
			pyxel.text(75, 75, "PUZZLE BATTLE", pyxel.COLOR_BLACK)
			self.draw_puzzle()
			self.draw_rule()

		elif self.phase == "SOLVE":
			self.draw_header()
			self.draw_puzzle()
			self.draw_rule()
			self.draw_rule_stack()

		elif self.phase == "TURN_RESULT":
			self.draw_header()
			self.draw_puzzle()
			self.draw_turn_result()
			self.draw_rule_stack()

		elif self.phase == "PUT_RULE":
			pyxel.text(75, 75, "PUT PUZZLE-RULE", pyxel.COLOR_BLACK)
			self.draw_header()
			self.draw_puzzle(self.rule_putting_idx)
			self.draw_rule()
			self.draw_rule_stack()

		elif self.phase == "RESULT":
			self.draw_result()


App()
