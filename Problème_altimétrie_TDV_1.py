#Olivier Moreau
#
#2025
#
#CQFA : Exam 1 : théorie du vol

import random

réponse = -1
alt_1 = 0
alt_2 = 0
alt_obst = 0

def alt() :

    if obstacle == False :

        alt_1 = random.randrange(0, 50001, 1000)
        alt_2 = random.randrange(0, 50001, 1000)

    elif obstacle == True :

        alt_1 = random.randrange(0, 50001, 1000)
        alt_2 = random.randrange(0, 50001, 1000)
        alt_obst = random.randrange(0, 50001, 1000)

    return alt_1, alt_2, alt_obst

def QNH() :

    

    if obstacle == False :

        QNH_1 = random.randrange(0, 50001, 1000)
        QNH_2 = random.randrange(0, 50001, 1000)

    elif obstacle == True :

        QNH_1 = random.randrange(0, 50001, 1000)
        QNH_2 = random.randrange(0, 50001, 1000)

    return QNH_1, QNH_2

while réponse <= -1 :

    #m ou pi
    nb_unité = random.randint(1,4)

    #obstacle
    nb_obstacle = random.randint(1,3)

    if nb_obstacle == 1 or nb_obstacle == 2 :

        obstacle = False

        if 1 <= nb_unité <= 3 :

            unité = "pi"

            alt()


        elif nb_unité == 4 :

            unité = "m"

            alt()

        réponse = 1

