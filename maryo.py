
#Import modules

import pygame, random, sys
from pygame.locals import *
pygame.init()
from PIL import Image, ImageDraw, ImageFont
import datetime
import pandas as pd
import random

try:
    df = pd.read_pickle('maryo_scores.pkl')
except:
    df = pd.DataFrame(columns=["lesson","presented_word","english_word","datetime","game_id","read_duration","killed","student_name"])
    df.to_pickle('maryo_scores.pkl')

df1 = pd.DataFrame(columns=["lesson","presented_word","english_word","datetime","game_id","read_duration","killed","student_name"])



reading_lookup_easy = {
    "!o": 'ō',
    "!a": "ā",
    "!e": "ē",
    "!i": "ï"
}
#next one needs to have the final length post char updates in the value locations
reading_lookup_hard = {
    "oo": 2,
    "sh": 2,
    "in-g": 3,
    "er": 2,
    "th": 2,
    "_e": 1,
    "_a": 1
}

reading_string = {"17":'''that rat is sad''',
"67":'''the cat that talk_ed . . 
a girl had a cat. sh!e lov_ed her cat. sh!e talk_ed to 
her cat. then the cat talk_ed to her. the girl said, "I must
b!e sl!e!epin-g. cats can not talk"
the cat said, "you talk to m!e. s!o I can talk to you."
the girl g!av_e the cat a big hug. "I never had a 
cat that talk_ed".
the cat said, "I never had a cat that talk_ed."
the girl and the cat talk_ed and talk_ed.
then a man c!ame to the park. h!e went up to 
the girl and said, "can I hav_e that cat?"
the cat said, "I will not g!o with you."
the man said, "I must b!e sl!e!epin-g. cats do not 
talk. I will l!e_ave this park." and h!e did.
the end . .
''',
"68":'''f!indin-g some fun on the moon . .
some girls went to the moon in a moon ship.
a girl said, "I will f!ind some fun." sh!e walk_ed 
and walk_ed. soon sh!e c!am_e to a cow.
the moon cow said, "w!e can hav_e lots of fun.
come with m!e." the girl went with the moon cow to a 
pool. the moon cow said, "this is how w!e have fun
on the moon." sh!e jump_ed into the pool. and the 
girl jump_ed into the pool.
the girl said, "it is fun to swim on the moon." s!o 
the girl and the cow went swimmin-g every d!ay. the 
girl did not tell the other girls sh!e went 
swimmin-g with a moon cow.
the end . .
''',
"69":'''the fat man that never c!am_e back
a man had an !old car. the !old car did not start.
s!o the man went down the r!o_ad. soon h!e c!am_e to a 
rat.
the rat said, "n!o. rats do not hav_e cars."
s!o the man went down the r!o_ad. soon h!e c!am_e to
a fat man. h!e said, "can you start an !old car?"
the fat man said, "yes. I can but I will not. I
am sittin-g and I l!ik_e to sit."
the man said, "you can sit in this car if you can 
start it."
s!o the fat man got in the car and m!ade the car 
start. h!e said, "I l!ik_e this !old car. I will t!ak_e
it down the r!o_ad and never come back."
the end
''',
"70": '''bill went fishi-ng
bill went fishin-g with the other b!oys. the
other b!oys had lots of fish, but bill did not get
n!in_e fish !or f!iv_e fish. h!e got a big !old bag.
the other b!oys m!ad_e fun of bill. they said, "w!e 
hav_e fish and you hav_e an !old bag."
bill was sad. but then h!e said, "wow. this bag
is fill_ed with g!old."
the other b!oys look_ed ins!id_e the bag. "wow,"
they said.
now bill was not sad. h!e said to the other b!oys,
"you hav_e lots of fish, but I hav_e lots and lots of
g!old. s!o I am rich."
this is the end.
'''
}

student_name = 'B'
current_lesson = "70"
#current_lesson = "17"
current_word_index = 123
#current_word_index = 0
max_speed = 7


for i in reading_lookup_easy.keys():
    reading_string[current_lesson] = reading_string[current_lesson].replace(i,reading_lookup_easy[i])


reading_string[current_lesson] = reading_string[current_lesson].replace('\n',' . . ').split()
reading_string = reading_string[current_lesson]



#intialising variables for ease

window_height=600 
window_width=1200

blue = (0,0,255)
black = (0,0,0)
white = (255, 255, 255)

last_correct_input = datetime.datetime.now()

random_string = ''
for _ in range(40):
    # Considering only upper and lowercase letters
    random_integer = random.randint(97, 97 + 26 - 1)
    flip_bit = random.randint(0, 1)
    # Convert to lowercase if the flip bit is on
    random_integer = random_integer - 32 if flip_bit == 1 else random_integer
    # Keep appending random characters using chr(x)
    random_string += (chr(random_integer))
game_id = random_string

total_reading_x_distance_traversed = 0


fps = 30
level = 0
addnewwordrate = 10 #200 #40 #200 # HIGHER IS SLOWER ORIGINAL WAS 20

#defining the required function

def update_score(presented_word, read_duration, killed):
    global student_name
    global game_id
    global df1
    global current_lesson
    presented_word = presented_word.replace('"','').replace('.','').lower()
    english_word = presented_word.replace('_','').replace('!','').replace('-','')
    
    timestamp = datetime.datetime.now()
    data = {
        "lesson": current_lesson,
        "presented_word": presented_word,
        "english_word": english_word,
        "datetime": timestamp,
        "game_id": game_id,
        "read_duration": read_duration.total_seconds(),
        "killed": killed,
        "student_name": student_name
    }
    df2 = pd.DataFrame([data])
    df1 = pd.concat([df1, df2])
    #df1.to_pickle('maryo_scores.pkl')

def save_score():
    global df
    global df1
    dfo = pd.concat([df, df1],sort=True)
    dfo.to_pickle('maryo_scores.pkl')
    #df1.to_pickle('maryo_scores_latest.pkl')  # use this line if you want to write over all previous scores
    print('saving')

class dragon:

    global firerect, imagerect, Canvas
    up = False
    down = True
    velocity = 1
    
    def __init__(self):
        self.image = load_image('dragon.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.right = window_width
        self.imagerect.top = window_height/2

    def update(self):
        
        if (self.imagerect.top < cactusrect.bottom):
            self.up = False
            self.down = True

        if (self.imagerect.bottom > firerect.top):
            self.up = True
            self.down = False
            
        if (self.down):
            self.imagerect.bottom += self.velocity

        if (self.up):
            self.imagerect.top -= self.velocity

        Canvas.blit(self.image, self.imagerect)

    def return_height(self):

        h = self.imagerect.top
        return h

class words:
    #words('test',Canvas)
    global reading_string
    global current_lesson
    global addnewwordrate
    wordspeed = 1
    global window_width

    def __init__(self, text, surface,speed):
        self.score_log_completed = False
        self.text = text
        scale = 2
        self.wordspeed = speed
        fntsize = 40 * scale
        fntwidth = fntsize/1.8
        textlen = len(text)
        self.txtwidth = int(fntwidth*(textlen+1))
        fnt = ImageFont.truetype('LiberationMono-Regular.ttf', fntsize)
        sml_fnt = ImageFont.truetype('LiberationMono-Regular.ttf', int(fntsize/1.5))
        image = Image.new("RGBA",(self.txtwidth,fntsize*2), (0,0,0,0))
        draw = ImageDraw.Draw(image)

        

        self.need_complex_draw = False
        for i in reading_lookup_hard.keys():
            if i in text: 
                #print('gunna be hard')
                self.need_complex_draw = True

        i=0
        while i < len(text):
            self.doesnt_match_hard = True
            for ii in reading_lookup_hard.keys():
                #print('checking', text[i:i+len(ii)],text[i:i+len(ii)] == ii)
                if text[i:i+len(ii)] == ii:
                    self.doesnt_match_hard = False
                    hardkey = ii
                    #print('hard',text[i:i+len(ii)])
            if self.doesnt_match_hard:
                #print(text[i])
                draw.text((fntwidth*i+10,10), text[i], font=fnt, fill=(255,255,255))
                #add the character to the image
            else:  #so it's hard
                if hardkey in ['oo','th',"er","sh"]:
                        draw.text((fntwidth*i+10,10), text[i], font=fnt, fill=(255,255,255))
                        draw.text((int(fntwidth*(i+.7)+10),10), text[i+1], font=fnt, fill=(255,255,255))
                elif hardkey in ['_e','_a']:
                    draw.text((fntwidth*i+10,10+(fntsize-int(fntsize/1.5))), text[i+1], font=sml_fnt, fill=(255,255,255))
                    text = text.replace(hardkey,hardkey.replace('_',''))
                    i -= 1 # to compensate for removing the _
                elif hardkey in ["in-g"]:
                    draw.text((fntwidth*i+10,10), text[i], font=fnt, fill=(255,255,255))
                    draw.text((int(fntwidth*(i+1)+10),10), text[i+1], font=fnt, fill=(255,255,255))
                    draw.text((int(fntwidth*(i+2)+10),10), text[i+3], font=fnt, fill=(255,255,255))
                    draw.text((int(fntwidth*(i+1.5)+10),10-int(fntsize*.8)), '_', font=fnt, fill=(255,255,255))
                    i -= 1 # to compensate for not printing the -
                    text = text.replace(hardkey,hardkey.replace('-',''))

                i += len(hardkey)-1
            i += 1

       
            
        mode = image.mode
        size = image.size
        data = image.tobytes('raw', mode)
        this_image = pygame.image.fromstring(data, image.size, mode)
        '''
        strFormat = 'RGBA'
        raw_str = image.tostring("raw", strFormat)
        this_image = pygame.image.fromstring(raw_str, image.size, strFormat)
        '''
        self.image = this_image
        self.imagerect = self.image.get_rect()
        self.height = int(window_height/2)
        self.surface = self.image # pygame.transform.scale(self.image, (20,20))
        self.imagerect = pygame.Rect(window_width - 106, self.height, 20, 20)
        

        '''
        textobj = font.render(text, 1, white)
        textrect = textobj.get_rect()
        textrect.topleft = (window_width,window_height/2)
        surface.blit(textobj, textrect)

        self.image = load_image('fireball.png')
        self.imagerect = self.image.get_rect()
        self.height = Dragon.return_height() + 20
        self.surface = textobj#pygame.transform.scale(self.image, (20,20))
        self.imagerect = pygame.Rect(window_width - 106, self.height, 20, 20)
        '''

    def update(self,create_from_scratch, speed,update_last_correct_input):
        self.wordspeed = speed
        self.imagerect.left -= self.wordspeed
        if create_from_scratch:
            scale = 2
            text = self.text
            
            fntsize = 40 * scale
            fntwidth = fntsize/1.8
            textlen = len(text)
            self.txtwidth = int(fntwidth*(textlen+1))
            fnt = ImageFont.truetype('LiberationMono-Regular.ttf', fntsize)
            sml_fnt = ImageFont.truetype('LiberationMono-Regular.ttf', int(fntsize/1.5))

            # create new image
            image = Image.new("RGBA",(self.txtwidth,fntsize*2), (0,0,0,0))
            draw = ImageDraw.Draw(image)
            #draw.text((10,10), self.text, font=fnt, fill=(0,255,0))

            
            
            self.need_complex_draw = False
            for i in reading_lookup_hard.keys():
                if i in text: 
                    #print('gunna be hard')
                    self.need_complex_draw = True

            i=0
            while i < len(text):
                self.doesnt_match_hard = True
                for ii in reading_lookup_hard.keys():
                    #print('checking', text[i:i+len(ii)],text[i:i+len(ii)] == ii)
                    if text[i:i+len(ii)] == ii:
                        self.doesnt_match_hard = False
                        hardkey = ii
                        #print('hard',text[i:i+len(ii)])
                if self.doesnt_match_hard:
                    #print(text[i])
                    draw.text((fntwidth*i+10,10), text[i], font=fnt, fill=(50,255,50))
                    #add the character to the image
                else:  #so it's hard
                    if hardkey in ['oo','th',"er","sh"]:
                        draw.text((fntwidth*i+10,10), text[i], font=fnt, fill=(50,255,50))
                        draw.text((int(fntwidth*(i+.7)+10),10), text[i+1], font=fnt, fill=(50,255,50))
                    elif hardkey in ['_e','_a']:
                        draw.text((fntwidth*i+10,10+(fntsize-int(fntsize/1.5))), text[i+1], font=sml_fnt, fill=(50,255,50))
                        text = text.replace(hardkey,hardkey.replace('_',''))
                        i -= 1 # to compensate for removing the _
                    elif hardkey in ["in-g"]:
                        draw.text((fntwidth*i+10,10), text[i], font=fnt, fill=(50,255,50))
                        draw.text((int(fntwidth*(i+1)+10),10), text[i+1], font=fnt, fill=(50,255,50))
                        draw.text((int(fntwidth*(i+2)+10),10), text[i+3], font=fnt, fill=(50,255,50))
                        draw.text((int(fntwidth*(i+1.5)+10),10-int(fntsize*.8)), '_', font=fnt, fill=(50,255,50))
                        i -= 1 # to compensate for not printing the -
                        text = text.replace(hardkey,hardkey.replace('-',''))

                    i += len(hardkey)-1
                i += 1



            mode = image.mode
            size = image.size
            data = image.tobytes('raw', mode)
            this_image = pygame.image.fromstring(data, image.size, mode)
            '''
            strFormat = 'RGBA'
            raw_str = image.tostring("raw", strFormat)
            this_image = pygame.image.fromstring(raw_str, image.size, strFormat)
            '''
            self.image = this_image
            #self.imagerect = self.image.get_rect()
            self.height = int(window_height/2)
            self.surface = self.image # pygame.transform.scale(self.image, (20,20))

    def collision(self):
        if self.imagerect.left == 0:
            #return True
            I_dont_want_to_kill_on_touching_word = True
        else:
            return False

class maryo:
    global moveup, movedown, gravity, cactusrect, firerect, moveleft, moveright, word_list
    speed = 10
    downspeed = 20

    def __init__(self):
        self.image = load_image('maryo.png')
        self.imagerect = self.image.get_rect()
        self.imagerect.topleft = (50,window_height/2)
        self.score = 0

    def update(self,spot):
        self.imagerect.right = spot

        if (moveup and (self.imagerect.top > cactusrect.bottom)):
            self.imagerect.top -= self.speed
            self.score += 1
            
        if (movedown and (self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom += self.downspeed
            self.score += 1
        
        if (moveleft and (self.imagerect.left > 0)):
            self.imagerect.right -= self.speed
            self.score -= 1
            
        if (moveright and (self.imagerect.right < window_width)):
            self.imagerect.right += self.downspeed
            self.score += 1
            
        if (gravity and (self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom += self.speed
        
        #drawTraj(Canvas,self.imagerect.bottom)



def terminate():        #to end the program
    save_score()
    pygame.quit()
    sys.exit()

def waitforkey():
    while True :                                        #to wait for user to start
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:     #to terminate if the user presses the escape key
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return
            
            

def wordhitsmario(playerrect, words):      #to check if word has hit mario or not
    for f in word_list:
        if playerrect.colliderect(f.imagerect):
            return True
        return False

def drawtext(text, font, surface, x, y):        #to display text on the screen
    textobj = font.render(text, 1, white)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


def check_level(score):
    global window_height, level, cactusrect, firerect
    if score in range(0,250):
        firerect.top = window_height - 50
        cactusrect.bottom = 50
        level = 1
    elif score in range(250, 500):
        firerect.top = window_height - 100
        cactusrect.bottom = 100
        level = 2
    elif score in range(500,750):
        level = 3
        firerect.top = window_height-150
        cactusrect.bottom = 150
    elif score in range(750,1000):
        level = 4
        firerect.top = window_height - 200
        cactusrect.bottom = 200

def load_image(imagename):
    return pygame.image.load(imagename)

    

#end of functions, begin to start the main code


mainClock = pygame.time.Clock()
Canvas = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('MARYO')

#setting up font and sounds and images

font = pygame.font.SysFont(None, 48)
scorefont = pygame.font.SysFont(None, 30)

fireimage = load_image('fire_bricks.png')
firerect = fireimage.get_rect()

cactusimage = load_image('cactus_bricks.png')
cactusrect = cactusimage.get_rect()

startimage = load_image('start.png')
startimagerect = startimage.get_rect()
startimagerect.centerx = window_width/2
startimagerect.centery = window_height/2

endimage = load_image('end.png')
endimagerect = startimage.get_rect()
endimagerect.centerx = window_width/2
endimagerect.centery = window_height/2

total_reading_x_distance_traversed = 0
next_word_x_distance_traversed = 0
last_correct_input = datetime.datetime.now()

player_dead_x = -10

pygame.mixer.music.load('mario_theme.wav')
gameover = pygame.mixer.Sound('mario_dies.wav')

#getting to the start screen

drawtext('Mario', font, Canvas,(window_width/3), (window_height/3))
Canvas.blit(startimage, startimagerect)

pygame.display.update()
waitforkey()

#start for the main code

topscore = 0
Dragon = dragon()

while True:

    word_list = []
    player = maryo()
    
    moveup = movedown = gravity = moveright = moveleft = judgement_state = want_right = False
    maryoIndex=0
    correctIndex=-1
    wordaddcounter = 0

    gameover.stop()
    #pygame.mixer.music.play(-1,0.0)

    

    while True:     #the main game loop
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:

                keys = pygame.key.get_pressed()

                if keys[pygame.K_a]:
                    if datetime.datetime.now() - last_correct_input > datetime.timedelta(milliseconds=200):
                        judgement_state = True
                
                if event.key == K_UP:
                    movedown = False
                    moveup = True
                    gravity = False

                if event.key == K_DOWN:
                    movedown = True
                    moveup = False
                    gravity = False
                
                if event.key == K_LEFT:
                    moveleft = True
                
                if event.key == K_RIGHT:
                    moveright = True
                    want_right = True

            if event.type == KEYUP:

                keys = pygame.key.get_pressed()

                if keys[pygame.K_a]:
                    judgement_state = False

                if event.key == K_UP:
                    moveup = False
                    #gravity = True
                if event.key == K_DOWN:
                    movedown = False
                    #gravity = True
                if event.key == K_LEFT:
                    moveleft = False
                    #gravity = True
                if event.key == K_RIGHT:
                    moveright = False
                    want_right = False
                    #gravity = True
                    
                if event.key == K_ESCAPE:
                    terminate()

        wordaddcounter += 1
        check_level(player.score)

        
        cur_speed = max_speed
        if len(word_list) > 0:
            cur_speed = max(1,int(word_list[maryoIndex].imagerect.left/(window_width*.66) * max_speed))
            cur_speed = min(max_speed, cur_speed)
        
        #print(wordaddcounter)
        if current_word_index < len(reading_string):
            if total_reading_x_distance_traversed >= next_word_x_distance_traversed:
                #get new word word
                newword = words(reading_string[current_word_index],Canvas,cur_speed)
                #calc next location
                next_word_x_distance_traversed = int(total_reading_x_distance_traversed + newword.txtwidth)
                print("total_reading_x_distance_traversed",total_reading_x_distance_traversed,"newword.txtwidth",newword.txtwidth,"next_word_x_distance_traversed",next_word_x_distance_traversed)
                current_word_index += 1
                word_list.append(newword)

        
        counter = 0
        for f in word_list:
            if counter < correctIndex:
                words.update(f,True,cur_speed,last_correct_input)  # draw it as completed and move left
                
                #now add it to the score df if not already there
                if not f.score_log_completed:
                    print('updating',f.score_log_completed,f.text)
                    update_score(f.text, datetime.datetime.now() - last_correct_input, 'no')
                    f.score_log_completed = True
                    last_correct_input = datetime.datetime.now()
            else:
                words.update(f,False,cur_speed,last_correct_input)  # otherwise just continue moving it left
            if judgement_state:
                print('bookmark: ', current_word_index - len(word_list))

                if correctIndex +1 < len(word_list):
                    correctIndex += 1
                    words.update(f,False,cur_speed,last_correct_input)  # mark it true and move left
                    
                judgement_state = False
            counter += 1
        
        total_reading_x_distance_traversed += cur_speed


        for f in word_list:
            if f.imagerect.left < player_dead_x:
                word_list.remove(f)
                correctIndex -= 1
                maryoIndex -= 1

        if want_right and maryoIndex < len(word_list) and maryoIndex < correctIndex:
            maryoIndex += 1
            want_right = False

        spot = 0
        #print("maryoIndex",maryoIndex)
        if len(word_list)>0 and maryoIndex < len(word_list):
            #print("maryoIndex",maryoIndex)
            spot = word_list[maryoIndex].imagerect.right

        player.update(spot)
        Dragon.update()
        

        Canvas.fill(black)
        Canvas.blit(fireimage, firerect)
        Canvas.blit(cactusimage, cactusrect)
        Canvas.blit(player.image, player.imagerect)
        Canvas.blit(Dragon.image, Dragon.imagerect)
        

        drawtext('Score : %s | Top score : %s | Level : %s' %(player.score, topscore, level), scorefont, Canvas, 350, cactusrect.bottom + 10)
        
        for f in word_list:
            Canvas.blit(f.surface, f.imagerect)

               

        if wordhitsmario(player.imagerect, word_list):
            '''if player.score > topscore:
                topscore = player.score
            break
            '''
            actually_do_nothing = True
        
        if ((player.imagerect.top <= cactusrect.bottom) or (player.imagerect.bottom >= firerect.top)):
            #if player.score > topscore:
            #    topscore = player.score
            #break
            dont_want_to_die = True
        if player.imagerect.left <= player_dead_x:
            print('ded')
            update_score(f.text, datetime.datetime.now() - last_correct_input, 'yes')
            #if player.score > topscore:
            #    topscore = player.score
            break
            #dont_want_to_die = True

        pygame.display.update()

        mainClock.tick(fps)
    
    pygame.mixer.music.stop()
    current_word_index = 0
    gameover.play()
    Canvas.blit(endimage, endimagerect)
    pygame.display.update()
    waitforkey()
