import pandas as pd
from datetime import date
import time
from selenium import webdriver
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import json

# Set up Chrome WebDriver with custom options
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--display=:99")  # Set display to Xvfb

# Google Sheets setup
SHEET_ID = '1RG-5uy_k3GbpDYINKDAZLh0UomU3U41N-Pk50Qtaus8'
SHEET_NAME1 = 'Reviews'  # Sheet to clear data below header and write new data

# Get Google Sheets credentials from environment variable
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
credentials = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))

# Create Google Sheets API service
service = build("sheets", "v4", credentials=credentials)

link_websites1 = [
    "https://www.airbnb.com/rooms/7146166",
    "https://www.airbnb.com/rooms/796474546246084466",
    "https://www.airbnb.com/rooms/37941371",
    "https://www.airbnb.com/rooms/994897495772736141",
    "https://www.airbnb.com/rooms/53642812",
    "https://www.airbnb.com/rooms/760854242202697132",
    "https://www.airbnb.com/rooms/51465037",
    "https://www.airbnb.com/rooms/53699752",
    "https://www.airbnb.com/rooms/1050859485309789128",
    "https://www.airbnb.com/rooms/53542247",
    "https://www.airbnb.com/rooms/892145528929581566",
    "https://www.airbnb.com/rooms/29828888",
    "https://www.airbnb.com/rooms/1075808915500918249",
    "https://www.airbnb.com/rooms/639093225461069229",
    "https://www.airbnb.com/rooms/1034850921926296677",
    "https://www.airbnb.com/rooms/30374855",
    "https://www.airbnb.com/rooms/862225236403589050",
    "https://www.airbnb.com/rooms/1095021360351651647",
    "https://www.airbnb.com/rooms/31572231",
    "https://www.airbnb.com/rooms/805787704495151180",
    "https://www.airbnb.com/rooms/1042003756371097226",
    "https://www.airbnb.com/rooms/31041744",
    "https://www.airbnb.com/rooms/724751471621735873",
    "https://www.airbnb.com/rooms/938322820404201166",
    "https://www.airbnb.com/rooms/842715702282301234",
    "https://www.airbnb.com/rooms/51464198",
    "https://www.airbnb.com/rooms/607805837215056615",
    "https://www.airbnb.com/rooms/29057616",
    "https://www.airbnb.com/rooms/28986286",
    "https://www.airbnb.com/rooms/30569087",
    "https://www.airbnb.com/rooms/30587914",
    "https://www.airbnb.com/rooms/726797791762309974",
    "https://www.airbnb.com/rooms/33297252",
    "https://www.airbnb.com/rooms/745517798832633224",
    "https://www.airbnb.com/rooms/783438310557347832",
    "https://www.airbnb.com/rooms/1079900607064150533",
    "https://www.airbnb.com/rooms/757905515382248564",
    "https://www.airbnb.com/rooms/21879855",
    "https://www.airbnb.com/rooms/557931274468753963",
    "https://www.airbnb.com/rooms/563061034458193391",
    "https://www.airbnb.com/rooms/897748901350874764",
    "https://www.airbnb.com/rooms/607996043990435730",
    "https://www.airbnb.com/rooms/655851097480261248",
    "https://www.airbnb.com/rooms/53935222",
    "https://www.airbnb.com/rooms/54003121",
    "https://www.airbnb.com/rooms/41926624",
    "https://www.airbnb.com/rooms/818808980294592759",
    "https://www.airbnb.com/rooms/910243374096737518",
    "https://www.airbnb.com/rooms/888535082546615005",
    "https://www.airbnb.com/rooms/53905490",
    "https://www.airbnb.com/rooms/805787804668716793",
    "https://www.airbnb.com/rooms/51444791",
    "https://www.airbnb.com/rooms/1076240628121073255",
    "https://www.airbnb.com/rooms/1031868725939524364",
    "https://www.airbnb.com/rooms/954991868458915427",
    "https://www.airbnb.com/rooms/1142996183974898781",
    "https://www.airbnb.com/rooms/1165972751097834093",
    "https://www.airbnb.com/rooms/570359369689296789",
    "https://www.airbnb.com/rooms/1113219669718192703",
    "https://www.airbnb.com/rooms/1136360425762834414",
    "https://www.airbnb.com/rooms/946617655515855386",
    "https://www.airbnb.com/rooms/834175163702868485",
    "https://www.airbnb.com/rooms/49612095",
    "https://www.airbnb.com/rooms/910164420748216135",
    "https://www.airbnb.com/rooms/990641443060144144",
    "https://www.airbnb.com/rooms/826137636518983708",
    "https://www.airbnb.com/rooms/949385102419491356",
    "https://www.airbnb.com/rooms/760969744755324887",
    "https://www.airbnb.com/rooms/1076968397509164945",
    "https://www.airbnb.com/rooms/1050127081836690246",
    "https://www.airbnb.com/rooms/26005379",
    "https://www.airbnb.com/rooms/786329086863037403",
    "https://www.airbnb.com/rooms/51963573",
    "https://www.airbnb.com/rooms/37932879",
    "https://www.airbnb.com/rooms/1076647410356569199",
    "https://www.airbnb.com/rooms/48318526",
    "https://www.airbnb.com/rooms/37938829",
    "https://www.airbnb.com/rooms/904360106135155927",
    "https://www.airbnb.com/rooms/803651754039471916",
    "https://www.airbnb.com/rooms/40083939",
    "https://www.airbnb.com/rooms/866663572875064288",
    "https://www.airbnb.com/rooms/1076647429394038254",
    "https://www.airbnb.com/rooms/25396298",
    "https://www.airbnb.com/rooms/26521913",
    "https://www.airbnb.com/rooms/23190272",
    "https://www.airbnb.com/rooms/838459330070610028",
    "https://www.airbnb.com/rooms/947760909472876352",
    "https://www.airbnb.com/rooms/861683985433638341",
    "https://www.airbnb.com/rooms/933446278486516018",
    "https://www.airbnb.com/rooms/800697914487131964",
    "https://www.airbnb.com/rooms/50212538",
    "https://www.airbnb.com/rooms/783452456583177550",
    "https://www.airbnb.com/rooms/1131831559412513348",
    "https://www.airbnb.com/rooms/981120989536057134",
    "https://www.airbnb.com/rooms/860831202321728447",
    "https://www.airbnb.com/rooms/978166940536444449",
    "https://www.airbnb.com/rooms/1042003712113364927",
    "https://www.airbnb.com/rooms/604398018806882504",
    "https://www.airbnb.com/rooms/1085699716941563659",
    "https://www.airbnb.com/rooms/782603780940799545",
    "https://www.airbnb.com/rooms/945044294292549232",
    "https://www.airbnb.com/rooms/1131831539618072124",
    "https://www.airbnb.com/rooms/944920764405587161",
    "https://www.airbnb.com/rooms/1030538591333449115",
    "https://www.airbnb.com/rooms/49343702",
    "https://www.airbnb.com/rooms/990031193822434771",
    "https://www.airbnb.com/rooms/957888455526887416",
    "https://www.airbnb.com/rooms/1050821870682745148",
    "https://www.airbnb.com/rooms/805787737386091039",
    "https://www.airbnb.com/rooms/777659652608777776",
    "https://www.airbnb.com/rooms/731243523553958261",
    "https://www.airbnb.com/rooms/782703665616562456",
    "https://www.airbnb.com/rooms/934235039382631269",
    "https://www.airbnb.com/rooms/1065769680885195405",
    "https://www.airbnb.com/rooms/1027936391154196841",
    "https://www.airbnb.com/rooms/973875354304828353",
    "https://www.airbnb.com/rooms/1008840674146919720",
    "https://www.airbnb.com/rooms/35681371",
    "https://www.airbnb.com/rooms/705127962698567441",
    "https://www.airbnb.com/rooms/756641747143688292",
    "https://www.airbnb.com/rooms/816076415461957447",
    "https://www.airbnb.com/rooms/755163388432693249",
    "https://www.airbnb.com/rooms/786951700961595417",
    "https://www.airbnb.com/rooms/1036993779134062225",
    "https://www.airbnb.com/rooms/853588629391260401",
    "https://www.airbnb.com/rooms/999220572832362368",
    "https://www.airbnb.com/rooms/908744644752740153",
    "https://www.airbnb.com/rooms/1047224654410054017",
    "https://www.airbnb.com/rooms/873999899483756758",
    "https://www.airbnb.com/rooms/873817166721037429",
    "https://www.airbnb.com/rooms/939783099662189198",
    "https://www.airbnb.com/rooms/955789623469064247",
    "https://www.airbnb.com/rooms/953562785617772309",
    "https://www.airbnb.com/rooms/887899763516426190",
    "https://www.airbnb.com/rooms/1021989674443871557",
    "https://www.airbnb.com/rooms/1039248371267406725",
    "https://www.airbnb.com/rooms/924821108022403394",
    "https://www.airbnb.com/rooms/968187624157610437",
    "https://www.airbnb.com/rooms/1022580739268065943",
    "https://www.airbnb.com/rooms/1148726239902098576",
    "https://www.airbnb.com/rooms/1015363142553312848",
    "https://www.airbnb.com/rooms/1106482531167089383",
    "https://www.airbnb.com/rooms/1097201811717296445",
    "https://www.airbnb.com/rooms/1009422704218853107",
    "https://www.airbnb.com/rooms/1008612218258117806",
    "https://www.airbnb.com/rooms/962985257513035512",
    "https://www.airbnb.com/rooms/1076780580862135211",
    "https://www.airbnb.com/rooms/834142836698095871",
    "https://www.airbnb.com/rooms/1050195214810043236",
    "https://www.airbnb.com/rooms/1097369463318457469",
    "https://www.airbnb.com/rooms/592728131979157301",
    "https://www.airbnb.com/rooms/886831553748022682",
    "https://www.airbnb.com/rooms/975448512532210038",
    "https://www.airbnb.com/rooms/995763813290807634",
    "https://www.airbnb.com/rooms/1047224676448180120",
    "https://www.airbnb.com/rooms/1103288077320277710",
    "https://www.airbnb.com/rooms/993606019538483430",
    "https://www.airbnb.com/rooms/623800381886559424",
    "https://www.airbnb.com/rooms/950908727734458240",
    "https://www.airbnb.com/rooms/47069678",
    "https://www.airbnb.com/rooms/29735607",
    "https://www.airbnb.com/rooms/1080557902929477424",
    "https://www.airbnb.com/rooms/1024760658855576495",
    "https://www.airbnb.com/rooms/50879442",
    "https://www.airbnb.com/rooms/897748881007679334",
    "https://www.airbnb.com/rooms/47054188",
    "https://www.airbnb.com/rooms/34473610",
    "https://www.airbnb.com/rooms/1153791334221199409",
    "https://www.airbnb.com/rooms/53830234",
    "https://www.airbnb.com/rooms/698162509016402967",
    "https://www.airbnb.com/rooms/894996626436696750",
    "https://www.airbnb.com/rooms/877628153832743245",
    "https://www.airbnb.com/rooms/785631343553027555",
    "https://www.airbnb.com/rooms/53951403",
    "https://www.airbnb.com/rooms/988528048108079239",
    "https://www.airbnb.com/rooms/53738223",
    "https://www.airbnb.com/rooms/715276271341771907",
    "https://www.airbnb.com/rooms/33988930",
    "https://www.airbnb.com/rooms/625973762731219742",
    "https://www.airbnb.com/rooms/1158812597782935422",
    "https://www.airbnb.com/rooms/46104590",
    "https://www.airbnb.com/rooms/43679726",
    "https://www.airbnb.com/rooms/1045634226433291187",
    "https://www.airbnb.com/rooms/25129364",
    "https://www.airbnb.com/rooms/31650019",
    "https://www.airbnb.com/rooms/953562785617772309",
    "https://www.airbnb.com/rooms/20842811",
    "https://www.airbnb.com/rooms/53188505",
    "https://www.airbnb.com/rooms/48939589",
    "https://www.airbnb.com/rooms/1060335247580958306",
    "https://www.airbnb.com/rooms/897963012858385842",
    "https://www.airbnb.com/rooms/25548573",
    "https://www.airbnb.com/rooms/1118085675466754285",
    "https://www.airbnb.com/rooms/1118085697437915657",
    "https://www.airbnb.com/rooms/33990781",
    "https://www.airbnb.com/rooms/1118748453825614028",
    "https://www.airbnb.com/rooms/32358587",
    "https://www.airbnb.com/rooms/1175583169188948074",
    "https://www.airbnb.com/rooms/28105157",
    "https://www.airbnb.com/rooms/874576033916222052",
    "https://www.airbnb.com/rooms/1042003843639500595",
    "https://www.airbnb.com/rooms/52617221",
    "https://www.airbnb.com/rooms/965959236038176496",
    "https://www.airbnb.com/rooms/1014534960594628050",
    "https://www.airbnb.com/rooms/34336916",
    "https://www.airbnb.com/rooms/36668728",
    "https://www.airbnb.com/rooms/1177271590148127455",
    "https://www.airbnb.com/rooms/33067595",
    "https://www.airbnb.com/rooms/54081691",
    "https://www.airbnb.com/rooms/33073575",
    "https://www.airbnb.com/rooms/955107616627638300",
    "https://www.airbnb.com/rooms/940638312300885619",
    "https://www.airbnb.com/rooms/823155460080163160",
    "https://www.airbnb.com/rooms/874058281090322337",
    "https://www.airbnb.com/rooms/881137986854850087",
    "https://www.airbnb.com/rooms/881138921809210265",
    "https://www.airbnb.com/rooms/889232271666476805",
    "https://www.airbnb.com/rooms/1127057220252352925",
    "https://www.airbnb.com/rooms/1127061396214828918",
    "https://www.airbnb.com/rooms/985576433639311786",
    "https://www.airbnb.com/rooms/751390625816660039",
    "https://www.airbnb.com/rooms/1049393737893008941",
    "https://www.airbnb.com/rooms/763115309438666807",
    "https://www.airbnb.com/rooms/720376585440505157",
    "https://www.airbnb.com/rooms/675364370940591304",
    "https://www.airbnb.com/rooms/971038139081369306",
    "https://www.airbnb.com/rooms/765333675463864639",
    "https://www.airbnb.com/rooms/1127068754740193330",
    "https://www.airbnb.com/rooms/697219047472579604",
    "https://www.airbnb.com/rooms/985491774123385924",
    "https://www.airbnb.com/rooms/959474348410918154",
    "https://www.airbnb.com/rooms/1108970575915708107",
    "https://www.airbnb.com/rooms/764807706737137386",
    "https://www.airbnb.com/rooms/1030522085440736837",
    "https://www.airbnb.com/rooms/969628264375924718",
    "https://www.airbnb.com/rooms/45549853",
    "https://www.airbnb.com/rooms/1076275611613180477",
    # Add more URLs as needed
]

DateToday = date.today()
UpdatedAt = DateToday.strftime("%Y-%m-%d")

reviews_data = []
data = []

for website in link_websites1:
    revweb = website + "/reviews?"
    driver = webdriver.Chrome(options=options)
    listing_id = website.split('/')[-1]
    driver.get(revweb)

    time.sleep(5)  # Wait for the page to load

    All_Reviews2 = driver.find_elements("xpath", """//div[@class="r1are2x1 atm_gq_1vi7ecw dir dir-ltr"]""")

    if All_Reviews2:

        # Locate the scrollable element, this needs to be the correct XPath for the reviews container
        try:
            scrollable_div = driver.find_element("xpath", '//div[@class="_17itzz4"]')
        except Exception as e:
            print(f"Could not locate scrollable element: {e}")
            driver.quit()
            continue

        # Scroll down until all reviews are loaded
        last_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_div)
        while True:
            # Scroll down
            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_div)

            # Wait for reviews to load
            time.sleep(3)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return arguments[0].scrollHeight;", scrollable_div)
            if new_height == last_height:
                break
            last_height = new_height

        All_Reviews = driver.find_elements("xpath", """//div[@class="r1are2x1 atm_gq_1vi7ecw dir dir-ltr"]""")

        for review in All_Reviews:

            name_element = review.find_element("xpath", ".//h2[@elementtiming='LCP-target']")
            name = name_element.text.strip()

            # Extract the date of review
            date_element = review.find_element("xpath",
                                               """.//div[contains(@class, "s78n3tv ")]""").text.split(
                '·')[1]
            date_review = date_element.strip().strip('\n,')

            # Extract the star rating
            star_element = review.find_element("xpath", ".//span[contains(text(), 'Rating,')]")
            star_review = star_element.text.strip().strip('Rating, ')

            Stayedat = ''

            content_element = review.find_element("xpath",
                                                  ".//div[@class='r1bctolv atm_c8_1sjzizj atm_g3_1dgusqm atm_26_lfmit2_13uojos atm_5j_1y44olf_13uojos atm_l8_1s2714j_13uojos dir dir-ltr']")
            content_review = content_element.text.strip()

            try:  # Extract the response content
                response_element = review.find_element("xpath",
                                                       ".//div[@data-testid='pdp-reviews-response']//div[contains(@style, 'line-height: 1.25rem')]")
                response_content = response_element.text.strip()
            except:

                response_content = ''

            try:  # Extract the response date
                response_date_element = review.find_element("xpath",
                                                            ".//div[@data-testid='pdp-reviews-response']//div[@class='s15w4qkt atm_c8_1w0928g atm_g3_1dd5bz5 atm_cs_6adqpa atm_7l_1wzk1hz dir dir-ltr']")
                response_date = response_date_element.text.strip()
            except:

                response_date = ''

                # Append the extracted data to the list
            reviews_data.append({
                "Listing ID": listing_id,
                'name': name,
                'date_review': date_review,
                'star_review': star_review,
                'Stayedat': Stayedat,
                'content_review': content_review,
                'response_content': response_content,
                'response_date': response_date,
                'UpdatedAt': UpdatedAt
            })

    else:
        name = 'Listing has no Review Content or Unavailable'
        date_review = ''
        star_review = ''
        Stayedat = ''
        content_review = ''
        response_content = ''
        response_date = ''

        # Append the extracted data to the list
        reviews_data.append({
            "Listing ID": listing_id,
            'name': name,
            'date_review': date_review,
            'star_review': star_review,
            'Stayedat': Stayedat,
            'content_review': content_review,
            'response_content': response_content,
            'response_date': response_date,
            'UpdatedAt': UpdatedAt
        })

df = pd.DataFrame(reviews_data)

# Clear all data below header in the "Review" sheet
service.spreadsheets().values().clear(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME1}!A2:Z"
).execute()

# Write new data to the "Review" sheet starting from row 2
service.spreadsheets().values().update(
    spreadsheetId=SHEET_ID,
    range=f"{SHEET_NAME1}!A2",
    valueInputOption="RAW",
    body={"values": df.values.tolist()}
).execute()
