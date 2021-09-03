
#Import modules

import pygame, random, sys
from pygame.locals import *
pygame.init()
from PIL import Image, ImageDraw, ImageFont
import datetime
import pandas as pd
import random
import time

try:
    df = pd.read_pickle('maryo_scores.pkl')
except:
    df = pd.DataFrame(columns=["lesson","presented_word","english_word","datetime","game_id","read_duration","killed","student_name",'max_speed'])
    df.to_pickle('maryo_scores.pkl')

df1 = pd.DataFrame(columns=["lesson","presented_word","english_word","datetime","game_id","read_duration","killed","student_name",'max_speed'])



reading_lookup_simple_letters = {
    "!o": 'ō',
    "!a": "ā",
    "!e": "ē"
}
#next one needs to have the final length post char updates in the value locations
reading_lookup_complex_letters = {
    "o-o": 2,
    "sh": 2,
    "in-g": 3,
    "e-r": 2,
    "t-h": 2,
    "w-h": 2,
    "_e": 1,
    "_a": 1,
    "_k": 1,
    "!i": 1,
    "!y": 1
}

reading_string = {
"15": '''mad at m!e
''',
"16": '''r!e_ad it.
''',
"17":'''that rat is sad''',
"18":'''sam is mad at m!e
''',
"19":'''s!e!e th!e ram sit
''',
"20":'''th!e ram is sad
''',
"21":'''this cat is sic_k. this cat is sad.
''',
"22":'''that is a s!e!ed. s!e!e a ram !e_at it.
''',
"23":'''this is a 
roc_k. sam is 
at th!e roc_k
''',
"24": '''''',
"25": '''''',
"26": '''a man sat 
on a ram. 
t-hat ram can 
not s!e!e 
''',
"28": """a sock is 
in th!e sun. 
t-h!e soc_k is 
on m!e.
""",
"29": """an ant can 
!e_at a s!e!ed. 
t-hat s!e!ed is 
in t-h!e mud. 
""",
"30": """ t-his is a cat. t-h!e cat can run. mud is on t-h!e cat. 
""",
"31": """a man sat in t-h!e sand. a littl_e ant can s!e!e th!e man. th!e ant is mad. 
""",
"67":'''the cat that talk_ed . . 
a girl had a cat. sh!e lov_ed he-r cat. sh!e talk_ed to 
he-r cat. then the cat talk_ed to he-r. the girl said, "I must
b!e sl!e!epin-g. cats can not talk"
the cat said, "you talk to m!e. s!o I can talk to you."
the girl g!av_e the cat a big hug. "I neve-r had a 
cat that talk_ed".
the cat said, "I neve-r had a cat that talk_ed."
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
the girl and the cow went swimmin-g eve-ry d!ay. the 
girl did not tell the othe-r girls sh!e went 
swimmin-g with a moon cow.
the end . .
''',
"69":'''the fat man that neve-r c!am_e back
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
it down the r!o_ad and neve-r come back."
the end
''',
"70": '''bill went fishi-ng
bill went fishin-g with the othe-r b!oys. the
othe-r b!oys had lots of fish, but bill did not get
n!in_e fish !or f!iv_e fish. h!e got a big !old bag.
the othe-r b!oys m!ad_e fun of bill. they said, "w!e 
hav_e fish and you hav_e an !old bag."
bill was sad. but then h!e said, "wow. this bag
is fill_ed with g!old."
the othe-r b!oys look_ed ins!id_e the bag. "wow,"
they said.
now bill was not sad. h!e said to the othe-r b!oys,
"you hav_e lots of fish, but I hav_e lots and lots of
g!old. s!o I am rich."
this is the end.
''',
"71": '''the fat !e_agl_e
ther_e was an !e_agl_e that was fat, fat, fat. the othe-r 
!e_agl_es m!ad_e fun of the fat !e_agl_e. they said, "you do 
not look l!ik_e an !e_agl_e. you look l!ik_e a fat rock." 
the fat !e_agl_e was sittin-g in a tr!e!e when a t!ige-r c!am_e 
huntin-g f!or !e_agl_es. that t!iger was g!oin-g to get a little 
wh!it_e !e_agl_e. the little wh!it_e !e_agl_e was under the fat 
!e_agl_e's tr!e!e. the other !e_agl_es yell_ed, but the little wh!it_e 
!e_agl_e did not h!e_ar them. 
the fat !e_agl_e look_ed at the t!iger gettin-g n!e_ar the 
wh!it_e !e_agl_e. then the fat !e_agl_e said, "I must s!av_e that 
wh!it_e !e_agl_e." s!o h!e jumped down. h!e c!am_e down on the t!ige-r 
l!ik_e a fat rock. that t!ige-r ran far aw!ay. the 
little wh!it_e !e_agl_e was s!av_ed. 
when the other !e_agl_es c!am_e !ove-r to the fat !e_agl_e, 
they said, "w!e will neve-r m!ak_e fun of you now." 
the end
''',
"72":'''the wh!it_e tooth brush 
a girl l!ik_ed to brush he-r t!e!eth. sh!e had a 
wh!it_e tooth brush that sh!e l!ik_ed. but sh!e did not 
s!e!e he-r wh!it_e tooth brush. sh!e look_ed for it. sh!e 
said to he-r mothe-r, "whe-r_e is m!y wh!it_e tooth brush?" 
he-r mothe-r said, "I do not hav_e it." 
the girl was walkin-g back to he-r room when sh!e fell down. sh!e 
fell !ove-r he-r dog. that dog was 
brushin-g his t!e!eth with he-r wh!it_e tooth brush. 
the girl said, "you hav_e m!y wh!it_e tooth brush." 
the dog said, "I l!ik_e t!e!eth that sh!in_e l!ik_e the 
moon."
when the girl look_ed at the dog's t!e!eth, sh!e sm!il_ed. 
then the dog sm!il_ed. the girl said, "w!e hav_e t!e!eth 
that a-r_e wh!it_e, wh!it_e, wh!it_e."
the dog said, "w!e hav_e t!e!eth that sh!in_e l!ik_e the 
moon." 
the end 
''',
"73":'''an !old h!ors_e and an !e_agl_e 
an !e_agl_e said to an !old h!ors_e, "I will t!e_ach 
you how to fl!y. the !e_agl_e went to the top of the 
wh!it_e barn. 
then the !e_agl_e said, "now you fl!y to the top of 
this barn." but the !old h!ors_e did not fl!y. h!e ran 
into the s!id_e of that barn. 
Then the !e_agl_e said, "I will fl!y to the top of 
that ca-r." and sh!e did. 
but the !old h!ors_e did not fl!y to the top of the 
ca-r. h!e ran into the s!id_e of the ca-r. h!e said, 
"m!y mothe-r and m!y brothe-r can not fl!y. I can 
not fl!y."
the !e_agl_e said, "when you fl!y, you can hav_e fun." 
the h!ors_e said, "I can run with an !e_agl_e on m!y 
back, and that is fun." 
so the !e_agl_e sat on the back of the !old h!ors_e, 
and the !old h!ors_e ran up a hill. when they got to 
the top of the hill, the !e_agl_e said, "yes, this is 
a lot of fun." 
this is the end. 
''',
"74":'''the fat man that never came back 
a man had an old car. the old car did not start. so 
the man went down the road. soon he came to a rat. 
the man said, "can you start an old car?" 
the rat said, "no. rats do not have cars." 
So the man went down the road. soon he came to a 
fat man. he said, "can you start an old car?" 
the fat man said, "yes, I can but I will not. I am 
sitting and I like to sit." 
the man said, "you can sit in this car if you can 
start it." 
so the fat man got in the car and made the car 
start. he said, "I like this old car. I will take it down 
the road and never come back." 
the end
''',
"75":'''bill went fishing
bill went fishing with the other boys. the other 
boys had lots of fish, but bill did not get nine fish or 
five fish. he got a big old bag. 
the other boys made fun of bill. they said, "we 
have fish and you have an old bag."
bill was sad. but then he said, "wow. this bag is 
filled with gold." 
the other boys looked inside the bag. "wow," they 
said.
now bill was not sad. he said to the other boys,
"you have lots of fish, but I have lots and lots of gold. 
so I am rich."
this is the end
''',
"76": '''the fat eagle
there was an eagle that was fat, fat, fat. the other 
eagles made fun of the fat eagle. they said, "you do not 
Looks like an eagle. you look like a fat rock." 
the fat eagle was sitting in a tree when a tiger 
came hunting for eagles. that tiger was going to get a 
little white eagle. the little white eagle was under the 
fat eagle's tree. the other eagles yelled, but the little 
white eagle did not hear them.
the fat eagle looked at the tiger getting near the 
white eagle. then the fat eagle said, "i must save that 
white eagle." so he jumped down. he came down on 
the tiger like a fat rock. that tiger ran far away. the 
little wihte eagle was saved. 
when the other eagles came over to the fat eagle, 
they said, "we will never make fun of you now."
the end 
'''
}
#suggested regex to quality check the paragraph you enter:
#(?<!th|!|_)e( |\.)|(?<!_)a(?!(n))|er|(?<!_)ed( |\.)|\S\n|my | her |shine|lik|ing | ov| smil|eagle|le | old|horse|[A-Z]|fly|hor|sid|cannot

student_name = 'O'  # 'Dad' 'B' 'O'
current_lesson = "76"
current_lesson = "31"
current_word_index = 0
#current_word_index = 0


if student_name == 'O':
    completion_color = (255,150,150)
    max_speed = 2
    min_speed = 1
elif student_name == "B":
    completion_color = (50,50,255)
    max_speed = 3
    min_speed = 1
else:
    completion_color = (50,255,50)
    max_speed = 3
    min_speed = 3
mega_speed = 30  # used when the kid gets to the right side of the screen

todays_reading_string = ''
for i in reading_lookup_simple_letters.keys():
    todays_reading_string = reading_string[current_lesson].replace(i,reading_lookup_simple_letters[i])


todays_reading_string = todays_reading_string.replace('\n',' . . ').split()




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
    global max_speed
    global current_lesson
    presented_word = presented_word.replace('"','').replace('.','').lower()
    english_word = presented_word.replace('_','').replace('!','').replace('-','').replace('?','').replace('ē','e').replace('ā','a').replace('ō','o')
    
    timestamp = datetime.datetime.now()
    data = {
        "lesson": current_lesson,
        "presented_word": presented_word,
        "english_word": english_word,
        "datetime": timestamp,
        "game_id": game_id,
        "read_duration": read_duration.total_seconds(),
        "killed": killed,
        "student_name": student_name,
        'max_speed': max_speed
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
    global todays_reading_string
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
        for i in reading_lookup_complex_letters.keys():
            if i in text: 
                #print('gunna be hard')
                self.need_complex_draw = True

        i=0
        while i < len(text):
            self.doesnt_match_hard = True
            for ii in reading_lookup_complex_letters.keys():
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
                if hardkey in ['oo','wh',"sh"]: #must be two characters long
                    if '-' in text:
                        text = text.replace('-','')
                    draw.text((fntwidth*i+10,10), text[i], font=fnt, fill=(255,255,255))
                    draw.text((int(fntwidth*(i+.7)+10),10), text[i+1], font=fnt, fill=(255,255,255))
                elif hardkey in ['e-r','t-h']: #must be two characters at the end of taking out the marker chars  # made separate because the rule before wasnt bringing htem close enough
                    if '-' in text:
                        text = text.replace('-','')
                    draw.text((fntwidth*i+10,10), text[i], font=fnt, fill=(255,255,255))
                    draw.text((int(fntwidth*(i+.7)+10),10), text[i+1], font=fnt, fill=(255,255,255))
                    i -= 1
                elif hardkey in ['_e','_a','_k']:
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
                elif hardkey in ["!y"]:
                        draw.text((int(fntwidth*(i)+10),10), text[i+1], font=fnt, fill=(255,255,255))
                        draw.text((int(fntwidth*(i)+10),10-int(fntsize*.7)), '_', font=fnt, fill=(255,255,255))
                        draw.text((int(fntwidth*(i)+10),10-int(fntsize*.675)), '_', font=fnt, fill=(255,255,255))
                        draw.text((int(fntwidth*(i)+10),10-int(fntsize*.65)), '_', font=fnt, fill=(255,255,255))
                        i -= 1 # to compensate for not printing the -
                        text = text.replace(hardkey,hardkey.replace('!',''))
                elif hardkey in ["!i"]:
                        draw.text((int(fntwidth*(i)+10),10), text[i+1], font=fnt, fill=(255,255,255))
                        draw.text((int(fntwidth*(i)+10),10-int(fntsize*.8)), '_', font=fnt, fill=(255,255,255))
                        i -= 1 # to compensate for not printing the -
                        text = text.replace(hardkey,hardkey.replace('!',''))

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
            for i in reading_lookup_complex_letters.keys():
                if i in text: 
                    #print('gunna be hard')
                    self.need_complex_draw = True

            i=0
            while i < len(text):
                self.doesnt_match_hard = True
                for ii in reading_lookup_complex_letters.keys():
                    #print('checking', text[i:i+len(ii)],text[i:i+len(ii)] == ii)
                    if text[i:i+len(ii)] == ii:
                        self.doesnt_match_hard = False
                        hardkey = ii
                        #print('hard',text[i:i+len(ii)])
                if self.doesnt_match_hard:
                    #print(text[i])
                    draw.text((fntwidth*i+10,10), text[i], font=fnt, fill=completion_color)
                    #add the character to the image
                else:  #so it's hard
                    if hardkey in ['oo','th','wh','e-r',"sh"]: #must be two characters long
                        if '-' in text:
                            text = text.replace('-','')
                        draw.text((fntwidth*i+10,10), text[i], font=fnt, fill=completion_color)
                        draw.text((int(fntwidth*(i+.7)+10),10), text[i+1], font=fnt, fill=completion_color)
                    elif hardkey in ['_e','_a','_k']:
                        draw.text((fntwidth*i+10,10+(fntsize-int(fntsize/1.5))), text[i+1], font=sml_fnt, fill=(255,255,255))
                        text = text.replace(hardkey,hardkey.replace('_',''))
                        i -= 1 # to compensate for removing the _
                    elif hardkey in ["in-g"]:
                        draw.text((fntwidth*i+10,10), text[i], font=fnt, fill=completion_color)
                        draw.text((int(fntwidth*(i+1)+10),10), text[i+1], font=fnt, fill=completion_color)
                        draw.text((int(fntwidth*(i+2)+10),10), text[i+3], font=fnt, fill=completion_color)
                        draw.text((int(fntwidth*(i+1.5)+10),10-int(fntsize*.8)), '_', font=fnt, fill=completion_color)
                        i -= 1 # to compensate for not printing the -
                        text = text.replace(hardkey,hardkey.replace('-',''))
                    elif hardkey in ["!y"]:
                        draw.text((int(fntwidth*(i)+10),10), text[i+1], font=fnt, fill=completion_color)
                        draw.text((int(fntwidth*(i)+10),10-int(fntsize*.7)), '_', font=fnt, fill=completion_color)
                        draw.text((int(fntwidth*(i)+10),10-int(fntsize*.675)), '_', font=fnt, fill=completion_color)
                        draw.text((int(fntwidth*(i)+10),10-int(fntsize*.65)), '_', font=fnt, fill=completion_color)
                        i -= 1 # to compensate for not printing the -
                        text = text.replace(hardkey,hardkey.replace('!',''))
                    elif hardkey in ["!i"]:
                            draw.text((int(fntwidth*(i)+10),10), text[i+1], font=fnt, fill=completion_color)
                            draw.text((int(fntwidth*(i)+10),10-int(fntsize*.8)), '_', font=fnt, fill=completion_color)
                            i -= 1 # to compensate for not printing the -
                            text = text.replace(hardkey,hardkey.replace('!',''))

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
    global moveup, movedown, gravity, cactusrect, firerect, moveleft, moveright, all_currently_displayed_words
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
            #self.score += 1
            
        if (movedown and (self.imagerect.bottom < firerect.top)):
            self.imagerect.bottom += self.downspeed
            #self.score += 1
        
        if (moveleft and (self.imagerect.left > 0)):
            self.imagerect.right -= self.speed
            #self.score -= 1
            
        if (moveright and (self.imagerect.right < window_width)):
            self.imagerect.right += self.downspeed
            #self.score += 1
            
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
    for f in all_currently_displayed_words:
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
cur_speed = max_speed
last_chocolate_chip_time = datetime.datetime.now()

while True:

    all_currently_displayed_words = []
    player = maryo()
    
    moveup = movedown = gravity = moveright = moveleft = judgement_state = want_right = False
    maryo_index=0
    next_unread_word_index=-1
    wordaddcounter = 0

    gameover.stop()
    pygame.mixer.music.play(-1,0.0)

    

    while True:     #the main game loop
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:

                keys = pygame.key.get_pressed()

                if keys[pygame.K_a]:
                    if datetime.datetime.now() - last_correct_input > datetime.timedelta(milliseconds=200):
                        last_correct_input = datetime.datetime.now()
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

        if cur_speed != mega_speed:
            cur_speed = max_speed
            if len(all_currently_displayed_words) > 0:
                cur_speed = max(min_speed,int(all_currently_displayed_words[maryo_index].imagerect.left/(window_width*.66) * max_speed))
                cur_speed = min(max_speed, cur_speed)
        
        #print(wordaddcounter)
        if current_word_index < len(todays_reading_string):  # this just catches the end of string condition
            if total_reading_x_distance_traversed >= next_word_x_distance_traversed:
                #get new word word
                newword = words(todays_reading_string[current_word_index],Canvas,cur_speed)
                #calc next location
                next_word_x_distance_traversed = int(total_reading_x_distance_traversed + newword.txtwidth)
                print("total_reading_x_distance_traversed",total_reading_x_distance_traversed,"newword.txtwidth",newword.txtwidth,"next_word_x_distance_traversed",next_word_x_distance_traversed)
                current_word_index += 1
                all_currently_displayed_words.append(newword)
                print("norm speed")
                cur_speed = max_speed
            elif len(all_currently_displayed_words) - 1 == maryo_index:
                cur_speed = mega_speed
                if datetime.datetime.now() - last_chocolate_chip_time > datetime.timedelta(seconds=6):
                    last_chocolate_chip_time = datetime.datetime.now()
                    player.score += 1


        
        counter = 0
        for f in all_currently_displayed_words:
            if counter < next_unread_word_index:
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
                print('bookmark: ', current_word_index - len(all_currently_displayed_words))

                if next_unread_word_index +1 < len(all_currently_displayed_words):
                    next_unread_word_index += 1
                    words.update(f,False,cur_speed,last_correct_input)  # mark it true and move left
                    
                judgement_state = False
            counter += 1
        
        total_reading_x_distance_traversed += cur_speed


        for f in all_currently_displayed_words:  # this for loop removes the words that have gone over the far left of the screen
            if f.imagerect.left < player_dead_x:
                all_currently_displayed_words.remove(f)
                next_unread_word_index -= 1
                maryo_index -= 1

        if want_right:
            print("maryo_index",maryo_index,"next_unread_word_index",next_unread_word_index)
        if want_right and maryo_index < next_unread_word_index:
            if maryo_index < len(all_currently_displayed_words):
                maryo_index += 1
                want_right = False
            
        spot = 0
        #print("maryo_index",maryo_index)
        if len(all_currently_displayed_words)>0 and maryo_index < len(all_currently_displayed_words):
            #print("maryo_index",maryo_index)
            spot = all_currently_displayed_words[maryo_index].imagerect.right

        player.update(spot)
        Dragon.update()
        

        Canvas.fill(black)
        Canvas.blit(fireimage, firerect)
        Canvas.blit(cactusimage, cactusrect)
        Canvas.blit(player.image, player.imagerect)
        Canvas.blit(Dragon.image, Dragon.imagerect)
        

        drawtext('Score : %s | Top score : %s | Level : %s' %(player.score, topscore, level), scorefont, Canvas, 350, cactusrect.bottom + 10)
        choco_image = load_image('chocolate_chip_vanilla.png')
        choco_image = pygame.transform.scale(choco_image, (20, 20))
        choco_image_imagerect = choco_image.get_rect()
        choco_image_imagerect.centerx = 330
        choco_image_imagerect.centery = cactusrect.bottom + 17
        Canvas.blit(choco_image, choco_image_imagerect)

        
        for f in all_currently_displayed_words:
            Canvas.blit(f.surface, f.imagerect)

               

        if wordhitsmario(player.imagerect, all_currently_displayed_words):
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
