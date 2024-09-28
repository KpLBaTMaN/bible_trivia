from enum import Enum

# Define an enum for the difficulty levels
class Difficulty(str, Enum):
    easy = 'easy'
    medium = 'medium'
    hard = 'hard'

# Define an enum for all the books of the Bible
class BibleBook(str, Enum):
    # Old Testament
    genesis = 'Genesis'
    exodus = 'Exodus'
    leviticus = 'Leviticus'
    numbers = 'Numbers'
    deuteronomy = 'Deuteronomy'
    joshua = 'Joshua'
    judges = 'Judges'
    ruth = 'Ruth'
    samuel_1 = '1 Samuel'
    samuel_2 = '2 Samuel'
    kings_1 = '1 Kings'
    kings_2 = '2 Kings'
    chronicles_1 = '1 Chronicles'
    chronicles_2 = '2 Chronicles'
    ezra = 'Ezra'
    nehemiah = 'Nehemiah'
    esther = 'Esther'
    job = 'Job'
    psalms = 'Psalms'
    proverbs = 'Proverbs'
    ecclesiastes = 'Ecclesiastes'
    song_of_solomon = 'Song of Solomon'
    isaiah = 'Isaiah'
    jeremiah = 'Jeremiah'
    lamentations = 'Lamentations'
    ezekiel = 'Ezekiel'
    daniel = 'Daniel'
    hosea = 'Hosea'
    joel = 'Joel'
    amos = 'Amos'
    obadiah = 'Obadiah'
    jonah = 'Jonah'
    micah = 'Micah'
    nahum = 'Nahum'
    habakkuk = 'Habakkuk'
    zephaniah = 'Zephaniah'
    haggai = 'Haggai'
    zechariah = 'Zechariah'
    malachi = 'Malachi'
    
    # New Testament
    matthew = 'Matthew'
    mark = 'Mark'
    luke = 'Luke'
    john = 'John'
    acts = 'Acts'
    romans = 'Romans'
    corinthians_1 = '1 Corinthians'
    corinthians_2 = '2 Corinthians'
    galatians = 'Galatians'
    ephesians = 'Ephesians'
    philippians = 'Philippians'
    colossians = 'Colossians'
    thessalonians_1 = '1 Thessalonians'
    thessalonians_2 = '2 Thessalonians'
    timothy_1 = '1 Timothy'
    timothy_2 = '2 Timothy'
    titus = 'Titus'
    philemon = 'Philemon'
    hebrews = 'Hebrews'
    james = 'James'
    peter_1 = '1 Peter'
    peter_2 = '2 Peter'
    john_1 = '1 John'
    john_2 = '2 John'
    john_3 = '3 John'
    jude = 'Jude'
    revelation = 'Revelation'

class Topics(str, Enum):
    # Genesis Topics
    joseph_story = "Joseph's Story"
    joseph_rise_to_power = "Joseph's Rise to Power"
    joseph_family_reunion = "Joseph's Family Reunion"
    joseph_forgiveness_and_reconciliation = "Joseph's Forgiveness and Reconciliation"
    gods_providence_and_sovereignty = "God's Providence and Sovereignty"
    joseph_dreams_and_interpretations = "Joseph's Dreams and Interpretations"
    jacobs_blessings_and_prophesies = "Jacob's Blessings and Prophecies"
    judahs_transformation_and_leadership = "Judah’s Transformation and Leadership"
    jacobs_last_days_and_blessings = "Jacob's Last Days and Blessings"

    # Zechariah Topics
    zechariah_visions = "Zechariah's Visions"
    zechariah_message_of_repentance = "Zechariah's Message of Repentance"
    zechariah_future_messianic_hope = "Zechariah's Future Messianic Hope"
    temple_rebuilding_and_restoration = "Temple Rebuilding and Restoration"
    god_and_israels_future = "God and Israel’s Future"
    priestly_and_royal_leadership = "Priestly and Royal Leadership"

    # Romans Topics
    justification_by_faith = "Justification by Faith"
    all_have_sinned = "All Have Sinned"
    gods_righteous_judgment = "God's Righteous Judgment"
    abrahams_faith_and_promise = "Abraham's Faith and Promise"
    peace_with_god_through_christ = "Peace with God through Christ"
    gods_kindness = "God's Kindness"
    union_with_christ = "Union with Christ"
    the_role_of_the_law = "The Role of the Law"
    struggle_with_sin_and_grace = "Struggle with Sin and Grace"
    life_in_the_spirit = "Life in the Spirit"
    gods_wrath_and_mercy = "God's Wrath and Mercy"
    gods_faithfulness_to_israel = "God’s Faithfulness to Israel"
    adam_and_christ_contrast = "Adam and Christ Contrast"



class Tag(str, Enum):
    # General Themes and Context
    old_testament = "old testament"
    new_testament = "new testament"
    
    # Family Dynamics and Relationships
    family = "family"
    jealousy = "jealousy"
    betrayal = "betrayal"
    reconciliation = "reconciliation"
    forgiveness = "forgiveness"
    blessings = "blessings"
    leadership = "leadership"
    legacy = "legacy"
    brotherhood = "brotherhood"
    parental_blessing = "parental blessing"
    sibling_rivalry = "sibling rivalry"
    
    # God's Plan, Providence, and Promises
    providence = "providence"
    sovereignty = "sovereignty"
    faith = "faith"
    promise = "promise"
    repentance = "repentance"
    restoration = "restoration"
    messianic_hope = "messianic hope"
    prophecy = "prophecy"
    visions = "visions"
    symbolism = "symbolism"
    covenant = "covenant"
    hope = "hope"
    deliverance = "deliverance"
    redemption = "redemption"
    
    # Dreams, Interpretations, and Spiritual Life
    dreams = "dreams"
    interpretation = "interpretation"
    spiritual_leadership = "spiritual leadership"
    priesthood = "priesthood"
    royal_leadership = "royal leadership"
    worship = "worship"
    temple = "temple"
    renewal = "renewal"
    holiness = "holiness"
    obedience = "obedience"
    
    # Theology of Salvation and Sin
    justification = "justification"
    grace = "grace"
    righteousness = "righteousness"
    mercy = "mercy"
    sin = "sin"
    law = "law"
    gospel = "gospel"
    salvation = "salvation"
    faithfulness = "faithfulness"
    judgment = "judgment"
    wrath = "wrath"
    baptism = "baptism"
    atonement = "atonement"
    new_life = "new life"
    sanctification = "sanctification"
    regeneration = "regeneration"
    reconciliation_with_god = "reconciliation with God"
    
    # Transformation, Struggles, and Spiritual Renewal
    struggle = "struggle"
    spiritual_battle = "spiritual battle"
    transformation = "transformation"
    # renewal = "renewal" # Already in Dreams, Interpretations, and Spiritual Life
    perseverance = "perseverance"
    endurance = "endurance"
    faith_and_works = "faith and works"
    suffering = "suffering"
    spiritual_identity = "spiritual identity"
    
    # Contrast and Comparison
    contrast = "contrast"
    adam_and_christ = "adam and christ"
    death_and_life = "death and life"
    law_and_grace = "law and grace"
    israel_and_gentiles = "israel and gentiles"
    
    # Miscellaneous
    exile = "exile"
    divine_promise = "divine promise"
    inheritance = "inheritance"
    divine_intervention = "divine intervention"
    reconciliation_with_brothers = "reconciliation with brothers"
    spiritual_restoration = "spiritual restoration"

