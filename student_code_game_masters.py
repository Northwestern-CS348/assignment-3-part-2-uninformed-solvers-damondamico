from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg1 = []
        peg2 = []
        peg3 = []
        for fact in self.kb.facts:
            if fact.statement.predicate == 'on':
                disk = fact.statement.terms[0].term.element
                diskindex = int(disk[-1])
                if fact.statement.terms[1].term.element == 'peg1':
                    peg1.append(diskindex)
                if fact.statement.terms[1].term.element == 'peg2':
                    peg2.append(diskindex)
                if fact.statement.terms[1].term.element == 'peg3':
                    peg3.append(diskindex)
        return (tuple(sorted(peg1)),tuple(sorted(peg2)),tuple(sorted(peg3)))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if self.isMovableLegal(movable_statement):
            disk = str(movable_statement.terms[0])
            source = str(movable_statement.terms[1])
            dest = str(movable_statement.terms[2])
            disksbelow = self.kb.kb_ask(parse_input('fact: (onTop ' + disk + ' ?x)'))
            desttop = self.kb.kb_ask(parse_input('fact: (top ?x ' + dest + ')'))
            self.kb.kb_retract(parse_input('fact: (on ' + disk + ' ' + source + ')'))
            self.kb.kb_assert(parse_input('fact: (on ' + disk + ' ' + dest + ')'))
            self.kb.kb_retract(parse_input('fact: (empty ' + dest + ')'))
            disksonsource = self.kb.kb_ask(parse_input('fact: (on ?x ' + source + ')'))
            if not disksonsource:
                self.kb.kb_assert(parse_input('fact: (empty ' + source + ')'))
            if desttop:
                oldtop = desttop[0].bindings[0].constant.element
                self.kb.kb_retract(parse_input('fact: (top ' + oldtop + ' ' + dest + ')'))
            self.kb.kb_retract(parse_input('fact: (top ' + disk + ' ' + source + ')'))
            self.kb.kb_assert(parse_input('fact: (top ' + disk + ' ' + dest + ')'))
            if disksbelow:
                belowdisks = []
                for LoB in disksbelow:
                    belowdisks.append(LoB.bindings[0].constant.element)
                smallest = belowdisks[0]
                for disk in belowdisks:
                    bound_smaller = self.kb.kb_ask(parse_input('fact: (smaller ' + smallest + ' ' + disk + ')'))
                    if not bound_smaller:
                        smallest = disk
                self.kb.kb_assert(parse_input('fact: (top ' + smallest + ' ' + source + ')'))





    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))
        gs = self.getGameState()


class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        y1 = [0,0,0]
        y2 = [0,0,0]
        y3 = [0,0,0]
        for fact in self.kb.facts:
            if fact.statement.predicate == 'coordinate':
                tile = fact.statement.terms[0].term.element
                number = tile[-1]
                if number == 'y':
                    number = -1
                else:
                    number = int(number)
                posx = int(fact.statement.terms[1].term.element[-1])
                if fact.statement.terms[2].term.element == 'pos1':
                    y1[posx - 1] = number
                if fact.statement.terms[2].term.element == 'pos2':
                    y2[posx - 1] = number
                if fact.statement.terms[2].term.element == 'pos3':
                    y3[posx - 1] = number
        return (tuple(y1), tuple(y2), tuple(y3))





    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        if self.isMovableLegal(movable_statement):
            tile = movable_statement.terms[0].term.element
            srcx = movable_statement.terms[1].term.element
            srcy = movable_statement.terms[2].term.element
            dstx = movable_statement.terms[3].term.element
            dsty = movable_statement.terms[4].term.element
            self.kb.kb_retract(parse_input('fact: (coordinate ' + tile + ' ' + srcx + ' ' + srcy + ')'))
            self.kb.kb_retract(parse_input('fact: (coordinate empty ' + dstx + ' ' + dsty + ')'))
            self.kb.kb_assert(parse_input('fact: (coordinate ' + tile + ' ' + dstx + ' ' + dsty + ')'))
            self.kb.kb_assert(parse_input('fact: (coordinate empty ' + srcx + ' ' + srcy + ')'))


        

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
