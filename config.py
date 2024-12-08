NUMPY_DRAWING_FOLDER_PATH = "./data/numpy_bitmap/"
BINARY_DRAWING_FOLDER_PATH = "./data/"
DRAWING_NAMES ="""airplane
alarm clock
ambulance
angel
ant
anvil
apple
arm
axe
backpack
banana
bandage
barn
baseball bat
basket
basketball
bat
bathtub
beach
bear
bed
bee
belt
bench
bicycle
binoculars
bird
birthday cake
book
boomerang
bottlecap
bowtie
bracelet
brain
bread
bridge
broccoli
broom
bucket
bulldozer
bus
bush
butterfly
cactus
cake
calculator
calendar
camel
camera
campfire
candle
cannon
canoe
car
carrot
castle
cat
cello
cell phone
chair
chandelier
church
clarinet
clock
cloud
compass
cookie
cooler
couch
cow
crab
crayon
crocodile
crown
cruise ship
cup
diamond
diving board
dog
dolphin
donut
door
dragon
drill
drums
duck
dumbbell
ear
elbow
elephant
envelope
eraser
eye
eyeglasses
face
fan
feather
fence
finger
fire hydrant
firetruck
fish
flamingo
flashlight
flip flops
floor lamp
flower
flying saucer
foot
fork
frog
frying pan
garden
garden hose
giraffe
goatee
golf club
grapes
grass
guitar
hamburger
hammer
hand
harp
hat
headphones
hedgehog
helicopter
hexagon
hockey puck
hockey stick
horse
hospital
hot air balloon
hot dog
hourglass
house
house plant
hurricane
ice cream
jacket
jail
kangaroo
key
keyboard
knee
knife
ladder
lantern
laptop
leaf
leg
light bulb
lighter
lighthouse
lightning
lion
lipstick
lobster
lollipop
mailbox
map
marker
matches
megaphone
mermaid
microphone
microwave
monkey
moon
mosquito
motorbike
mountain
mouse
mouth
mug
mushroom
nail
necklace
nose
ocean
octagon
octopus
onion
oven
owl
paintbrush
palm tree
panda
pants
paper clip
parachute
parrot
passport
peanut
pear
peas
pencil
penguin
piano
pig
pillow
pineapple
pizza
pliers
popsicle
postcard
potato
power outlet
purse
rabbit
raccoon
radio
rain
rainbow
rake
remote control
rhinoceros
rifle
river
roller coaster
rollerskates
sailboat
sandwich
saw
saxophone
scissors
scorpion
screwdriver
sea turtle
see saw
shark
sheep
shoe
shorts
shovel
sink
skateboard
skull
skyscraper
sleeping bag
smiley face
snail
snake
snorkel
snowflake
snowman
soccer ball
sock
spider
spoon
spreadsheet
square
squirrel
stairs
star
steak
stereo
stethoscope
stitches
stop sign
strawberry
streetlight
submarine
suitcase
sun
swan
sweater
swing set
sword
syringe
table
teapot
teddy-bear
television
tennis racquet
tent
The Eiffel Tower
The Great Wall of China
The Mona Lisa
tiger
toaster
toe
toilet
tooth
toothbrush
toothpaste
tornado
tractor
traffic light
train
tree
triangle
trombone
truck
trumpet
t-shirt
umbrella
underwear
vase
violin
washing machine
watermelon
waterslide
whale
wheel
windmill
wine bottle
wine glass
wristwatch
yoga
zebra""".split("\n")
FILENAME_PREFIX = ""

LOAD_DRAWINGS_FROM_EACH_FILE = 1000
TRAIN_PROPORTION = 0.7

DRAWING_IMAGE_SIZE = (
        28, # x
        28, # y
        1, # z (color channel count)
)

RANDOM_SEED = 2343223490

TRAIN_EPOCHS = 10