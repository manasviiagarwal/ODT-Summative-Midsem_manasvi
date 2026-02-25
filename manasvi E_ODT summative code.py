from machine import Pin, PWM
import neopixel
import time
import random

bpb = Pin(18, Pin.IN, Pin.PULL_UP)
ypb = Pin(19, Pin.IN, Pin.PULL_UP)
np = neopixel.NeoPixel(Pin(25), 16)
ser=PWM(Pin(32), freq = 50)

#function for each round

def rounds(nround, gtime):
    print("ROUND", nround)

    # blinking 3 times before showing the safe area
    x = 0
    while x < 3:
        for i in range(0, 16):
            np[i] = (0,255,0)
            np.write()
        time.sleep(0.2)

        for i in range(0, 16):
            np[i] = (0,0,0)
            np.write()
        time.sleep(0.2)

        x += 1

    time.sleep(2)

    r = random.randint(1,15)
    clr = random.randint(0,1)   # 0 = blue, 1 = yellow

    # green LEDs
    for i in range(0, r):
        np[i] = (0, 255, 0)
        np.write()
        time.sleep(gtime)

    # show safe LED
    if clr == 0:
        np[r] = (0,0,255)
    else:
        np[r] = (255,255,0)
    np.write()

    correct = False
    wrong = False

    # button checking
    for _ in range(6):
        if bpb.value()==0 and ypb.value()==0:
            wrong = True

        elif clr == 0 and bpb.value()==0:
            correct = True
            break
        elif clr == 1 and ypb.value()==0:
            correct = True
            break

        elif clr == 0 and ypb.value()==0:
            wrong = True
            break
        elif clr == 1 and bpb.value()==0:
            wrong = True
            break
        else:
            wrong = True

        time.sleep(0.1)

    return correct, r

while True:
    ser.duty(75)
    score = 0
    x = 0
    for i in range(0,16):
        np[i] = (0,0,0)
        np.write()

    name = input("hi what is your name: ")
    print("hi ", name, "welcome to ESCAPE THE SHARK!\nThe rules are simple: The NeoPixel lights move until one led randomly indicates yellow(land) or blue(water)\nshowing which area is safe. You must quickly press the matching button.\nEach round gets faster, and you lose if you press the wrong button or miss the timing.\nAfter three rounds, you will know if you escaped.")
    time.sleep(20)

    
    # ROUND 1  (time = 1 second)
    
    correct, r = rounds(1, 1)

    if correct:
        print("YAY! YOU ESCAPED!")
        for i in range(r+1, 16):
            np[i] = (0,255,0)
            np.write()
            time.sleep(0.2)
        score += 1
    else:
        print("One step closer to your end......")
        for i in range(0,16):
            np[i] = (255,0,0)
            np.write()
        time.sleep(2)

    for i in range(16):
        np[i] = (0, 0, 0)
        np.write()
    time.sleep(2)


    # ROUND 2  (time = 0.6 sec)
   
    correct, r = rounds(2, 0.6)

    if correct:
        print("YAY! YOU ESCAPED!")
        for i in range(r+1, 16):
            np[i] = (0,255,0)
            np.write()
            time.sleep(0.2)
        score += 1
    else:
        print("One step closer to your end......")
        for i in range(0,16):
            np[i] = (255,0,0)
            np.write()
        time.sleep(1)

    for i in range(16):
        np[i] = (0, 0, 0)
        np.write()
    time.sleep(2)

   
    # ROUND 3  (time = 0.4 sec)
   
    correct, r = rounds(3, 0.4)

    if correct:
        print("YAY! YOU ESCAPED!")
        for i in range(r+1, 16):
            np[i] = (0,255,0)
            np.write()
            time.sleep(0.2)
        score += 1
    else:
        print("One step closer to your end......")
        for i in range(0,16):
            np[i] = (255,0,0)
            np.write()
        time.sleep(1)

    for i in range(16):
        np[i] = (0, 0, 0)
        np.write()
    time.sleep(2)

    # finish + scoring
    print("GAME FINISHED....CALCULATING YOUR SCORE....")
    time.sleep(2)
    print("YOUR SCORE IS: ", score)
    time.sleep(1)

    if score >= 2:
        print("CONGRATS YOU ESCAPED")
        for l in range(75,126):
            ser.duty(l)
            time.sleep(0.05)
    else:
        print("LOSER!! YOU JUST BECAME SHARK'S LUNCH")
        for l in range(75,24,-1):
            ser.duty(l)
            time.sleep(0.05)

    for i in range(0,16):
        np[i] = (0,0,0)
        np.write()

    time.sleep(2)
    z = input(name + " do you want to play again?(yes/no): ")
    if z.lower() != "yes":
        print("ok bye")
        ser.duty(75)
        break