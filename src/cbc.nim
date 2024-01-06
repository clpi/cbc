# This is just an example to get you started. A typical binary package
# uses this file as the main entry point of the application.

import tables, algorithm, sets, random, sequtils, strformat, strscans, strutils

const Infinity = 1_000_000_000

const lMargin = 0
type
  Cell = object
    isMine: bool
    display: char
  Grid = seq[seq[Cell]]
  Game = object
    grid: Grid
    mineCount: Natural
    minesMarked: Natural
    isOver: bool

proc initGame(m, n: Positive): Game =
  result.grid = newSeqWith(m, repeat(Cell(isMine: false, display: '.'), n))
  let min = toInt(float(m * n) * 0.1)
  let max = toInt(float(m * n) * 0.2)
  result.mineCount = min + rand(max - min)
  var rm = result.mineCount
  while rm > 0:
    let x = rand(m - 1)
    let y = rand(n - 1)
    if not result.grid[x][y].isMine:
      dec rm
      result.grid[x][y].isMine = true
  result.minesMarked = 0

template `[]`(grid: Grid; x, y: int): Cell = grid[x][y]

iterator cells(grid: var Grid): var Cell =
  for y in 0..grid[0].high:
    for x in 0..grid.high:
      yield grid[x, y]

proc display(game: Game; endOfGame: bool) =
  let margin = repeat(' ', lMargin)
  echo margin, "\x1b[32;2m", toSeq(1..game.grid.len).join "  ", "\x1b[0m"
  for y in 0..game.grid[0].high:
    for x in 0..game.grid.high:
      let disp = case game.grid[x][y].display
      of '.': "30;2m."
      of 'x': "31;1mx" 
      of 'Y': "33;1mY"
      of 'N': "31;1mN"
      of ' ': "0m "
      of '1': "34m1"
      of '2': "36m2"
      of '3': "33m3"
      of '4': "31m4"
      of '5': "35m5"
      of '6': "32m6"
      of '?': "32;1m?"
      else: "37;2m"
      stdout.write "\x1b[", disp, "\x1b[0m  "
    stdout.write margin, "\x1b[32;2m", $(y + 1), "\x1b[0m  "
    stdout.write("\n")
  if not endOfGame:
    echo &"\x1b[0m\x1b[30;2mStats: \x1b[0m\x1b[31;1m{game.mineCount}\x1b[0m\x1b[31m mines\x1b[0m \x1b[32;1m{game.minesMarked} \x1b[0m\x1b[32mmarked\x1b[0m"
  
proc terminate(game: var Game; msg: string) =   
  game.isOver = true
  echo msg
  var ans = ""
  while ans notin ["y", "n"]:
    stdout.write "Another game (y/n)?"
    ans = try: stdin.readLine().toLowerAscii
      except EOFError: "n"
    if ans == "y":
      game = initGame(game.grid.len, game.grid[0].len)
      game.display false

proc resign(game: var Game) =
  var found = 0
  for cell in game.grid.cells:
    if cell.isMine:
      if cell.display == '?':
        cell.display = 'Y'
        inc found
      elif cell.display == 'x':
        cell.display = 'N'
  game.display true
  let msg = &"You found {found} of {game.mineCount} mines"
  game.terminate msg

proc markCell(game: var Game; x, y: int) =
  if game.grid[x, y].display == '?':
    dec game.minesMarked
    game.grid[x, y].display = '.'
  elif game.grid[x, y].display == '.':
    inc game.minesMarked
    game.grid[x, y].display = '?'

proc countAdjMines(game: Game; x, y: Natural): int =
  for j in (y - 1)..(y + 1):
    if j in 0..game.grid[0].high:
      for i in (x - 1)..(x + 1):
        if i in 0..game.grid.high:
          if game.grid[i, j].isMine:
            inc result

proc clearCell(g: var Game; x, y: int): bool =
  if x in 0..g.grid.high and y in 0..g.grid[0].high:
    if g.grid[x, y].display == '.':
      if g.grid[x, y].isMine:
        g.grid[x][y].display = 'x'
        echo "You lost!"
        return false
      let c = g.countAdjMines(x, y)
      if c > 0:
        g.grid[x][y].display = chr(ord('0') + c)
      else:
        g.grid[x][y].display = ' '
        for dx in -1..1:
          for dy in -1..1:
            if dx != 0 or dy != 0:
              discard g.clearCell(x + dx, y + dy)
  result = true

proc testForWin(g: var Game): bool =
  if g.minesMarked != g.mineCount: return false
  for c in g.grid.cells:
    if c.display == '.': return false
  result = true
  echo "You win!"

proc splitAction(g: Game; action: string): tuple[x, y: int; ok: bool] =
  var cmd: string
  if not action.scanf("$w $s$i $s$i$s$.", cmd, result.x, result.y): return
  if cmd.len != 1: return
  case cmd[0]:
  of 'c', 'm':
    if result.x notin 1..g.grid.len or result.y notin 1..g.grid[0].len: 
      g.display true
      echo &"Invalid coordinates: ({result.x}, {result.y})"
      echo &"Valid coordinates are: (1, 1) to ({g.grid.len}, {g.grid.len})"
      return
  else:
    echo &"Invalid command: '{cmd}'"
    return
  result.ok = true

proc printUsage() =
  echo "h or ?\t\tPrint this help"
  echo "c x y \t\tClear cell (x, y)"
  echo "m x y \t\tMark (toggle) cell (x,y)"
  echo "n x y \t\tStart new game with grid (x, y)"
  echo "q     \t\tQuit or resign game\n"
  echo "'x' = horizontal column number"
  echo "'y' = vertical row number\n"

when isMainModule:
  randomize()
  printUsage()

  var g = initGame(10, 9)
  g.display false
  while not g.isOver:
    stdout.write "\n\x1b[32;2;1mAction \x1b[33m→\x1b[0m\x1b[33m  "
    let action = try: stdin.readLine().toLowerAscii
      except EOFError: "q"
    case action[0]
    of 'h', '?': printUsage()
    of 'n':
      g = initGame(10, 9)
      g.display false
    of 'c':
      let (x, y, ok) = g.splitAction action
      if not ok: continue
      if g.clearCell(x - 1, y - 1):
        g.display false
        if g.testForWin(): g.resign()
      else:
        g.resign()
    of 'm':
      let (x, y, ok) = g.splitAction action
      if not ok: continue
      g.markCell(x - 1, y - 1)
      g.display false
      if g.testForWin(): g.resign()
    of 'q':
      g.resign()
    else:
      printUsage()
      g.display true
      continue
      
