##############################################################################
##############################################################################
##
## Program        : Craps Statistics
##
## Author         : Richard E. Pattis
##                  Computer Science Department
##                  University of California, Irvine
##                  Irvine, CA 92617-3435
##                  e-mail: pattis@ics.uci.edu
##
## Maintainer     : Author
##
##
## Description:
##
##    Craps prompts the user to enter the number of games to play. It then
##  plays (simulates) that many games of craps, keeping the win/loss
##  information. At the end, it displays these statistics.
##
##    Craps is a dice game. The thrower loses if he/she immediately rolls a 2
##  (snake eyes), 3, or 12 (box cars). The thrower wins if he/she immediately
##  rolls a 7 or 11. If the thrower does not immediately win or lose, the number
##  thrown becomes the 'point'. Afterwards, the thrower tries to make his/her
##  point by rolling that same value again (and winning) before rolling a 7
##  (and losing). When trying to make his/her point, the thrower keeps rolling
##  if he/she rolls any number other than the point or 7.
##
##
## Known Bugs     : None
##
## Future Plans   : None
##
## Program History:
##   8/ 8/00: R. Pattis - Operational in C++
##   5/15/01: R. Pattis - Translated to Java
##   5/16/01: R. Pattis - Changed identifiers to conform to Java style
##   3/ 6/13: R. Pattis - Converted to Python
##
##############################################################################
##############################################################################



from goody     import irange
from dice      import Dice
from stopwatch import Stopwatch
import prompt
import predicate

 
win_count     = 0                            #Win/Lose/Dice Statistics
lose_count    = 0

dice          = Dice([6,6])
game_timer    = Stopwatch()

games_to_play = prompt.for_int('Enter # of games to play', is_legal=predicate.is_positive, error_message='an int, but not > 0')

game_timer.start()
dice.standard_rolls_for_debugging()
for game in irange(1, games_to_play):        #Each iteration plays one game
    first_roll = dice.roll().pip_sum()       #Roll the dice and record their pip sum

    #Based on firstRoll, decide how to continue:
    #  immediate win/loss or trying to make point
    if first_roll == 7 or first_roll == 11:
        win_count += 1                       #Win on the first roll with 7 or 11

    elif first_roll == 2 or first_roll == 3 or first_roll == 12:
        lose_count += 1                      #Lose on the first roll with 2, 3, or 12

    else:                                    #Try to make the point as the game continues
        point = first_roll                   #point will never store 7, 11, 2, 3, or 12

        while(True):                         #Roll until roll point (win) or 7 (lose)
            roll = dice.roll().pip_sum()

            if roll == point:                #If made the point first
                win_count += 1               #...win and this game is over
                break
            elif roll == 7:                  #If roll a 7 first
                lose_count+= 1               #...lose and this game is over
                break
game_timer.stop();


##Display Statistics

print('  Raw Wins/Lose =', '{:,}'.format(win_count), '/', '{:,}'.format(lose_count))
print('  % Wins/Lose   =', 100.0*win_count/(win_count+lose_count), '/', 100.0*lose_count/(win_count+lose_count))
print()

print('  Dice Thrown   =', '{:,}'.format(dice.rolls()))
print('  Avg Dice/game =', dice.rolls()/games_to_play)
print()

print('  Elapsed Time  =' , game_timer.read(), 'seconds')
print('  Speed         =', '{:,}'.format(int(games_to_play/game_timer.read())), 'games/second')
