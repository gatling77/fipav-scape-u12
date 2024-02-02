import unittest 
from standings import Team, Score, Match, Championship

class StamndingsTest(unittest.TestCase):
    
    def setUp(self):
        self.local = Team("CDA")
        self.guest = Team("Olimpia Volley")
        self.other = Team("luraghese")
        self._3to2 = score = Score(3,2)
        self._3to1 = score = Score(3,1)
        self._3to0 = score = Score(3,0)
        self._0to3 = score = Score(0,3)
        self._1to3 = score = Score(1,3)
        self._2to3 = score = Score(2,3)

    def test_score_init_valid_input(self):
        score = Score(3,2)

    def test_score_init_invalid_input(self):
        with self.assertRaises(ValueError):
            Score(4,2)
        with self.assertRaises(ValueError):
            Score(-1,2)
        with self.assertRaises(ValueError):
            Score(3,4)
        with self.assertRaises(ValueError):
            Score(2,-1)

    def test_match_winner(self):
        
        andata = Match(self.local, self.guest, self._3to2)
        self.assertEqual(self.local, andata.winner())

        ritorno = Match(self.local,self.guest, self._2to3)
        self.assertEqual(self.guest, ritorno.winner())

    def test_match_points_for_invalid_team(self):
        match = Match(self.local, self.guest, self._3to2)
        with self.assertRaises(ValueError):
            match.points_for(self.other)

    def test_match_points_for_winner(self):
        match = Match(self.local, self.guest, self._3to2)
        self.assertEqual(match.points_for(self.local),2)
        self.assertEqual(match.points_for(self.guest),1)

        match = Match(self.local, self.guest, self._3to1)
        self.assertEqual(match.points_for(self.local),3)
        self.assertEqual(match.points_for(self.guest),0)

        match = Match(self.local, self.guest, self._3to0)
        self.assertEqual(match.points_for(self.local),3)
        self.assertEqual(match.points_for(self.guest),0)

        match = Match(self.local, self.guest, self._0to3)
        self.assertEqual(match.points_for(self.local),0)
        self.assertEqual(match.points_for(self.guest),3)

        match = Match(self.local, self.guest, self._1to3)
        self.assertEqual(match.points_for(self.local),0)
        self.assertEqual(match.points_for(self.guest),3)

        match = Match(self.local, self.guest, self._2to3)
        self.assertEqual(match.points_for(self.local),1)
        self.assertEqual(match.points_for(self.guest),2)
    
    def test_championship_team_list(self):
        c = Championship("1977-27-12")
        self.assertEqual(len(c.team_list()),0)
        t1 = Team("T1")
        t2 = Team("T2")
        t3 = Team("T3")
        t4 = Team("T4")

        m1 = Match(t1,t2,self._3to2)
        m2 = Match(t1,t3,self._3to2)
        m3 = Match(t2,t4,self._3to2)

        c.add_match(m1).add_match(m2).add_match(m3)

        self.assertEqual(len(c.team_list()),4)

    def test_championship_stats(self):
        c = Championship("1977-27-12")
        t1 = Team("T1")
        t2 = Team("T2")
        t3 = Team("T3")
        t4 = Team("T4")
        c.add_match(Match(t1,t2,self._3to2))
        c.add_match(Match(t1,t3,self._3to2))
        c.add_match(Match(t1,t4,self._3to0))
        c.add_match(Match(t2,t3,self._3to0))
        c.add_match(Match(t2,t4,self._0to3))
        c.add_match(Match(t2,t1,self._2to3))
        c.add_match(Match(t3,t4,self._3to0))
        
        # T1 = 12 pts, 4 win, 3 win 3-2
        print(c.stats())

if __name__=='__main__':
	unittest.main()