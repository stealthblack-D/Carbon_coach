"""
knowledge.py - Conversational knowledge base and natural language intelligence for Carbon Coach.
Provides detailed, scientific, and educational explanations for climate, sustainability,
renewable energy, and campus decarbonization topics in English, Telugu, and Hindi.
"""

from typing import Optional, Dict, Any, Tuple
from carbon_coach.multilingual import LANG_EN, LANG_TE, LANG_HI

# Comprehensive knowledge topics mapped to keyword triggers
KNOWLEDGE_TOPICS = {
    "carbon_footprint": {
        "keywords": ["what is carbon footprint", "what is a carbon footprint", "define carbon footprint", "explain carbon footprint", "కార్బన్ పాదముద్ర", "కార్బన్ ఫుట్‌ప్రింట్", "कार्बन पदचिह्न", "कार्बन फुटप्रिंट क्या"],
        "en": (
            "🌍 **What is a Carbon Footprint?**\n\n"
            "A **carbon footprint** represents the total volume of greenhouse gases—predominantly carbon dioxide ($CO_2$) and methane ($CH_4$)—emitted directly or indirectly by our daily actions, measured in kilograms or metric tons of **$CO_2$ equivalent ($CO_2e$)**.\n\n"
            "### Where Does It Come From?\n"
            "Every modern activity carries an invisible carbon cost:\n"
            "• **Mobility & Travel:** Burning fossil fuels in petrol cars ($0.171\\text{ kg/km}$), flights, and auto-rickshaws.\n"
            "• **Electricity & Power:** Coal-fired thermal power plants supplying the grid ($0.713\\text{ kg/kWh}$ in India).\n"
            "• **Food Systems:** Livestock farming, fertilizer manufacturing, and refrigerated transport.\n"
            "• **Waste & Goods:** Methane released from decomposing landfill waste and energy used in manufacturing plastic and electronics.\n\n"
            "### The Global & National Context\n"
            "• **Indian National Daily Average:** $\\approx 5.2\\text{ kg } CO_2e\\text{ / person / day}$ (World Bank / CEA).\n"
            "• **Global Daily Average:** $\\approx 13.0\\text{ kg } CO_2e\\text{ / person / day}$.\n"
            "• **Paris Climate Goal (2030):** Under $5.5\\text{ kg / day}$ globally to limit planetary warming to $1.5^\\circ\\text{C}$.\n\n"
            "🌱 *Tracking your footprint helps you identify high-emission blind spots and take targeted action to reduce your impact.*"
        ),
        "te": (
            "🌍 **కార్బన్ ఫుట్‌ప్రింట్ (Carbon Footprint) అంటే ఏమిటి?**\n\n"
            "కార్బన్ ఫుట్‌ప్రింట్ అనేది మన రోజువారీ పనుల వల్ల వాతావరణంలోకి విడుదలయ్యే మొత్తం గ్రీన్‌హౌస్ వాయువుల (ముఖ్యంగా కార్బన్ డయాక్సైడ్ మరియు మీథేన్) పరిమాణం. దీనిని **kg $CO_2e$** లో కొలుస్తారు.\n\n"
            "### ఇది ఎక్కడి నుండి వస్తుంది?\n"
            "• **ప్రయాణాలు:** పెట్రోల్ కార్లు, బైకులు, బస్సులు లేదా విమానాల ద్వారా ఇంధనం దహనం.\n"
            "• **విద్యుత్ వినియోగం:** భారతదేశంలో ఎక్కువ విద్యుత్ బొగ్గు ఆధారిత పవర్ ప్లాంట్ల ద్వారా ఉత్పత్తి అవుతుంది ($0.713\\text{ kg/kWh}$).\n"
            "• **ఆహారం & ఆహారపు అలవాట్లు:** మాంసాహారోత్పత్తి, ఆహార రవాణా మరియు ఎరువులు.\n"
            "• **వ్యర్థాలు:** చెత్త డంపింగ్ యార్డుల్లో కుళ్ళిపోయే వ్యర్థాల నుండి మీథేన్ విడుదల.\n\n"
            "భారతదేశంలో ఒక సగటు వ్యక్తి రోజుకు దాదాపు **$5.2\\text{ kg } CO_2e$** విడుదల చేస్తాడు. మన అలవాట్లను మార్చుకోవడం ద్వారా దీనిని సులభంగా తగ్గించవచ్చు!"
        ),
        "hi": (
            "🌍 **कार्बन फुटप्रिंट (Carbon Footprint) क्या है?**\n\n"
            "कार्बन फुटप्रिंट हमारे दैनिक जीवन और गतिविधियों द्वारा वातावरण में उत्सर्जित कुल ग्रीनहाउस गैसों (विशेष रूप से कार्बन डाइऑक्साइड और मीथेन) का माप है, जिसे **किलोग्राम $CO_2e$** में मापा जाता है।\n\n"
            "### इसके मुख्य स्रोत क्या हैं?\n"
            "• **परिवहन:** पेट्रोल/डीजल कारों, दोपहिया वाहनों और उड़ानों में जीवाश्म ईंधन का जलना।\n"
            "• **बिजली खपत:** भारत में बिजली ग्रिड का बड़ा हिस्सा कोयले पर आधारित है ($0.713\\text{ kg/kWh}$)।\n"
            "• **भोजन:** मांस उत्पादन, डेयरी और खाद्य प्रसंस्करण।\n"
            "• **कचरा:** लैंडफिल में कचरे के सड़ने से निकलने वाली मीथेन गैस।\n\n"
            "भारत में प्रति व्यक्ति औसत दैनिक उत्सर्जन लगभग **$5.2\\text{ kg } CO_2e$** है। इसे ट्रैक करने से हमें उत्सर्जन कम करने के सही रास्ते मिलते हैं।"
        ),
    },

    "climate_change": {
        "keywords": ["what causes climate change", "causes of climate change", "why is climate changing", "explain climate change", "క్లైమేట్ చేంజ్", "వాతావరణ మార్పు", "जलवायु परिवर्तन के कारण", "जलवायु परिवर्तन क्या"],
        "en": (
            "🌡️ **What Causes Climate Change?**\n\n"
            "Climate change is primarily driven by the **enhanced greenhouse effect** caused by human industrial activity over the past 150 years.\n\n"
            "### Primary Drivers:\n"
            "1. **Burning Fossil Fuels (Coal, Oil, Natural Gas):**\n"
            "   Accounting for over $75\\%$ of global greenhouse gas emissions and nearly $90\\%$ of all carbon dioxide emissions, fossil fuel combustion for electricity, heating, and transport traps solar heat in the lower atmosphere.\n\n"
            "2. **Deforestation & Land Clearing:**\n"
            "   Forests act as natural carbon sinks. When trees are cut or burned for agriculture and urbanization, their stored carbon is released back into the air, and Earth's capacity to absorb $CO_2$ diminishes.\n\n"
            "3. **Industrial Agriculture & Livestock:**\n"
            "   Cattle farming generates huge quantities of **methane ($CH_4$)**, a greenhouse gas over 28 times more potent than $CO_2$ over a 100-year timescale. Synthetic nitrogen fertilizers emit nitrous oxide ($N_2O$).\n\n"
            "4. **Industrial Manufacturing & Cement Production:**\n"
            "   Chemical reactions in steel, cement, and chemical manufacturing release massive volumes of process emissions.\n\n"
            "💡 *The result:* Rising global temperatures, intensifying heatwaves, erratic monsoons, melting polar glaciers, and sea-level rise."
        ),
        "te": (
            "🌡️ **వాతావరణ మార్పులకు (Climate Change) కారణాలు ఏమిటి?**\n\n"
            "వాతావరణ మార్పులకు మానవ కార్యకలాపాల వల్ల పెరుగుతున్న **గ్రీన్‌హౌస్ ప్రభావం** ప్రధాన కారణం.\n\n"
            "### ముఖ్యమైన కారణాలు:\n"
            "1. **శిలాజ ఇంధనాల దహనం:** విద్యుత్, కర్మాగారాలు మరియు రవాణా కోసం బొగ్గు, పెట్రోల్ మరియు డీజిల్ వాడకం వల్ల పెద్ద ఎత్తున $CO_2$ విడుదలవుతుంది.\n"
            "2. **అడవుల నరికివేత:** చెట్లు గాలిలోని కార్బన్‌ను గ్రహించి నిల్వ చేస్తాయి. అడవులను నరికివేసినప్పుడు ఆ కార్బన్ మళ్లీ వాతావరణంలోకి విడుదలవుతుంది.\n"
            "3. **రసాయన ఎరువులు మరియు పశుపోషణ:** మిథేన్ మరియు నైట్రస్ ఆక్సైడ్ వంటి శక్తివంతమైన వాయువులు విడుదలవుతాయి.\n"
            "4. **పారిశ్రామిక వ్యర్థాలు:** సిమెంట్, ప్లాస్టిక్ మరియు ఉక్కు తయారీ కర్మాగారాల నుండి ఉద్గారాలు.\n\n"
            "దీని ఫలితంగా అధిక ఉష్ణోగ్రతలు, అకాల వర్షాలు, కరువులు మరియు సముద్ర మట్టాలు పెరుగుతున్నాయి."
        ),
        "hi": (
            "🌡️ **जलवायु परिवर्तन (Climate Change) के क्या कारण हैं?**\n\n"
            "जलवायु परिवर्तन का मुख्य कारण मानव गतिविधियों द्वारा वातावरण में ग्रीनहाउस गैसों का अत्यधिक जमाव है।\n\n"
            "### प्रमुख कारण:\n"
            "1. **जीवाश्म ईंधनों का जलना:** बिजली, उद्योगों और वाहनों के लिए कोयला, पेट्रोल और प्राकृतिक गैस जलाने से $75\\%$ से अधिक ग्रीनहाउस गैसें निकलती हैं।\n"
            "2. **वनों की कटाई:** जंगल प्राकृतिक रूप से कार्बन को सोखते हैं। पेड़ों के कटने से कार्बन दोबारा हवा में मिल जाता है।\n"
            "3. **गहन कृषि और पशुपालन:** मवेशियों से मीथेन गैस और रासायनिक उर्वरकों से नाइट्रस ऑक्साइड निकलती है।\n"
            "4. **औद्योगिक अपशिष्ट:** सीमेंट और इस्पात उत्पादन की रासायनिक प्रक्रियाएं।\n\n"
            "इसके परिणाम हैं: भीषण गर्मी, अनियमित मानसून, बाढ़ और ग्लेशियरों का पिघलना।"
        ),
    },

    "harmful_emissions": {
        "keywords": ["why are carbon emissions harmful", "why is carbon bad", "dangers of co2", "harm of carbon", "కార్బన్ ఎందుకు హానికరం", "కార్బన్ ఉద్గారాలు", "कार्बन उत्सर्जन हानिकारक क्यों", "कार्बन क्यों बुरा"],
        "en": (
            "⚠️ **Why Are Carbon Emissions Harmful?**\n\n"
            "While carbon dioxide ($CO_2$) is a natural constituent of Earth's atmosphere, excess emissions produced by burning trapped subterranean carbon disrupt Earth's thermal equilibrium:\n\n"
            "### 1. The Blanket Effect (Global Warming)\n"
            "Excess $CO_2$ acts as a heat-trapping blanket around the Earth. Sunlight penetrates the atmosphere, but heat radiating back from Earth's surface cannot escape into space, steadily raising the planet's baseline temperature.\n\n"
            "### 2. Ocean Acidification\n"
            "The world's oceans absorb roughly $30\\%$ of human $CO_2$ emissions. This reacts with seawater to form carbonic acid, dissolving coral reefs and threatening the shell-forming organisms that underpin the marine food chain.\n\n"
            "### 3. Extreme Weather & Food Insecurity\n"
            "Higher temperatures fuel more violent cyclones, prolonged droughts, and erratic monsoons, severely damaging agricultural yields and threatening water security for billions.\n\n"
            "### 4. Public Health Risks\n"
            "Fossil fuel combustion releases particulate matter ($PM_{2.5}$), sulfur dioxide ($SO_2$), and nitrogen oxides alongside $CO_2$, contributing to chronic respiratory conditions and cardiovascular disease."
        ),
        "te": (
            "⚠️ **కార్బన్ ఉద్గారాలు ఎందుకు హానికరం?**\n\n"
            "కార్బన్ డయాక్సైడ్ అధికంగా విడుదల కావడం భూమికి మరియు జీవకోటికి అనేక విధాలుగా నష్టం కలిగిస్తుంది:\n\n"
            "1. **భూతాపం పెరగడం:** గాలిలో $CO_2$ పొరలా మారి భూమి నుండి తిరిగి వెళ్లే ఉష్ణాన్ని ఆపివేస్తుంది, దీనివల్ల భూమి వేడెక్కుతుంది.\n"
            "2. **సముద్రాల ఆమ్లీకరణం:** సముద్రాలు $CO_2$ ను పీల్చుకోవడం వల్ల నీటిలో ఆమ్ల శాతం పెరిగి పగడపు దిబ్బలు మరియు సముద్ర జీవులు నాశనమవుతాయి.\n"
            "3. **తీవ్రమైన ప్రకృతి వైపరీత్యాలు:** తుఫానులు, కరువులు మరియు పంట నష్టాలు పెరిగి ఆహార కొరత ఏర్పడుతుంది.\n"
            "4. **ఆరోగ్య సమస్యలు:** శిలాజ ఇంధనాల నుండి వచ్చే కాలుష్యం వల్ల ఆస్తమా మరియు శ్వాసకోశ వ్యాధులు పెరుగుతాయి."
        ),
        "hi": (
            "⚠️ **कार्बन उत्सर्जन हानिकारक क्यों है?**\n\n"
            "अत्यधिक कार्बन उत्सर्जन पृथ्वी के पर्यावरण और मानव स्वास्थ्य के लिए गंभीर खतरा है:\n\n"
            "1. **ग्लोबल वार्मिंग:** $CO_2$ वातावरण में एक कंबल की तरह काम करता है, जो गर्मी को अंतरिक्ष में जाने से रोकता है और पृथ्वी का तापमान बढ़ाता है।\n"
            "2. **समुद्रों का अम्लीकरण:** समुद्री जल $CO_2$ सोखकर अम्लीय हो रहा है, जिससे समुद्री जीवन और प्रवाल भित्तियों (Coral Reefs) को नुकसान पहुँचता है।\n"
            "3. **चरम मौसम:** बेमौसम बारिश, सूखा, और भयंकर तूफानों की आवृत्ति बढ़ रही है।\n"
            "4. **स्वास्थ्य संकट:** जीवाश्म ईंधन से निकलने वाले वायु प्रदूषक सांस और फेफड़ों की गंभीर बीमारियों का कारण बनते हैं।"
        ),
    },

    "reduce_footprint": {
        "keywords": ["how can i reduce my carbon footprint", "how to reduce footprint", "reduce carbon", "ways to reduce emissions", "కార్బన్ ఎలా తగ్గించాలి", "కార్బన్ తగ్గింపు", "कार्बन पदचिह्न कैसे घटाएं", "कार्बन कम करने के उपाय"],
        "en": (
            "💡 **How Can You Reduce Your Carbon Footprint?**\n\n"
            "Achieving meaningful reductions does not require drastic lifestyle upheaval—smart, consistent daily adjustments yield immense compounded savings:\n\n"
            "### 1. High-Impact Mobility Switches\n"
            "• **Choose Public Transit or Metro:** Switching a $10\\text{ km}$ solo car commute to metro or bus cuts emissions by up to $82\\%$ (saves $\\approx 1.42\\text{ kg } CO_2e\\text{ / trip}$).\n"
            "• **Embrace Active Commuting:** Walking or cycling produce **$0.000\\text{ kg } CO_2e$** and improve cardiovascular health.\n"
            "• **Carpooling:** Sharing rides with peers divides per-person vehicle emissions by 3 to 4.\n\n"
            "### 2. Smart Electricity Habits\n"
            "• **AC Thermostat Optimization:** Set your air conditioner to $24^\\circ\\text{C} - 26^\\circ\\text{C}$ instead of $18^\\circ\\text{C}$. Every $1^\\circ\\text{C}$ increase saves $6\\%$ electricity ($\approx 0.43\\text{ kg } CO_2e\\text{ / hour}$ on 1.5-ton units).\n"
            "• **Eliminate Phantom Loads:** Switch off appliances, chargers, and monitors at the wall socket when not in use.\n"
            "• **Switch to LEDs:** LED lighting uses $80\\%$ less power than incandescent and compact fluorescent bulbs.\n\n"
            "### 3. Mindful Food Choices\n"
            "• **Increase Plant-Rich Meals:** Swapping one red meat meal for lentils, dal, or paneer eliminates up to $5.1\\text{ kg } CO_2e$ per meal (Poore & Nemecek Oxford study).\n"
            "• **Prevent Food Waste:** Decomposing food waste in landfills produces potent methane gas.\n\n"
            "### 4. Circular Waste Practices\n"
            "• **Segregate at Source:** Recycling plastic, paper, and metal earns carbon avoidance credits under EPA WARM guidelines.\n"
            "• **Compost Organics:** Composting organic matter aerobically avoids anaerobic methane generation."
        ),
        "te": (
            "💡 **మీ కార్బన్ పాదముద్రను ఎలా తగ్గించుకోవచ్చు?**\n\n"
            "సులభమైన రోజువారీ మార్పులతో మీరు మీ ఉద్గారాలను గణనీయంగా తగ్గించవచ్చు:\n\n"
            "### 1. ప్రయాణ అలవాట్లు మార్చడం\n"
            "• వ్యక్తిగత కారు లేదా బైక్ కంటే బస్సు, మెట్రో లేదా రైలును ఎంచుకోండి.\n"
            "• చిన్న దూరాలకు నడక లేదా సైకిల్ వాడండి (0.0 kg ఉద్గారాలు).\n"
            "• కళాశాల లేదా ఆఫీసుకు కార్‌పూలింగ్ చేయండి.\n\n"
            "### 2. విద్యుత్ ఆదా చేయడం\n"
            "• ఏసీ ఉష్ణోగ్రతను $24^\\circ\\text{C} - 26^\\circ\\text{C}$ వద్ద ఉంచండి (ప్రతి $1^\\circ\\text{C}$ పెరుగుదలకు 6% విద్యుత్ ఆదా).\n"
            "• అవసరం లేనప్పుడు ఫ్యాన్లు, లైట్లు మరియు ఛార్జర్లను స్విచ్ ఆఫ్ చేయండి.\n"
            "• సాధారణ బల్బుల స్థానంలో LED లైట్లను ఉపయోగించండి.\n\n"
            "### 3. ఆహారంలో మార్పులు\n"
            "• శాకాహారం లేదా పప్పుదినుసులను ఎక్కువగా తీసుకోవడం వల్ల ఉద్గారాలు తగ్గుతాయి.\n"
            "• అన్నం మరియు కూరగాయల వ్యర్థాలను వృధా చేయకండి.\n\n"
            "ఈ మార్పులతో మీరు నెలకు కనీసం 50 నుండి 100 kg కార్బన్‌ను ఆదా చేయవచ్చు!"
        ),
        "hi": (
            "💡 **आप अपना कार्बन पदचिह्न (Carbon Footprint) कैसे घटा सकते हैं?**\n\n"
            "दैनिक जीवन में छोटे और समझदारी भरे बदलाव करके आप बड़ा प्रभाव डाल सकते हैं:\n\n"
            "### 1. परिवहन में सुधार\n"
            "• अकेले कार चलाने के बजाय मेट्रो, बस या लोकल ट्रेन का उपयोग करें।\n"
            "• छोटी दूरी के लिए पैदल चलें या साइकिल चलाएं (शून्य उत्सर्जन)।\n"
            "• दोस्तों और सहकर्मियों के साथ कारपूलिंग करें।\n\n"
            "### 2. ऊर्जा और बिजली की बचत\n"
            "• एसी को $24^\\circ\\text{C} - 26^\\circ\\text{C}$ पर चलाएं। हर $1^\\circ\\text{C}$ बढ़ाने पर लगभग $6\\%$ बिजली बचती है।\n"
            "• उपयोग न होने पर चार्जर, लैपटॉप और लाइटों को स्विच ऑफ करें।\n"
            "• पुराने बल्बों की जगह ऊर्जा-कुशल LED लाइट्स लगाएं।\n\n"
            "### 3. आहार और कचरा प्रबंधन\n"
            "• भोजन की बर्बादी रोकें और पौधे-आधारित (शाकाहारी) भोजन को प्राथमिकता दें।\n"
            "• प्लास्टिक और कागज को रीसायकल करें तथा जैविक कचरे से खाद (कंपोस्ट) बनाएं।"
        ),
    },

    "renewable_energy": {
        "keywords": ["explain renewable energy", "what is renewable energy", "types of renewable energy", "solar energy", "పునరుత్పాదక శక్తి", "సౌర విద్యుత్", "नवीकरणीय ऊर्जा क्या", "अक्षय ऊर्जा"],
        "en": (
            "☀️ **What is Renewable Energy?**\n\n"
            "**Renewable energy** is energy derived from natural, self-replenishing resources that are virtually inexhaustible and produce near-zero operational greenhouse gas emissions.\n\n"
            "### The Core Technologies:\n"
            "1. **Solar Photovoltaic (PV) & Thermal:**\n"
            "   Converts sunlight directly into electrical current using silicon semiconductor cells. India possesses exceptional solar irradiance with $300+$ sunny days annually.\n\n"
            "2. **Wind Energy:**\n"
            "   Modern multi-megawatt turbines convert aerodynamic kinetic energy of moving air masses into electrical power.\n\n"
            "3. **Hydroelectric Power:**\n"
            "   Harnesses gravitational water flow through hydraulic turbines to generate clean base-load and peaking power.\n\n"
            "4. **Green Hydrogen & Biomass:**\n"
            "   Extracting fuel via water electrolysis powered by renewables to decarbonize heavy industry like steel and chemical fertilizer production.\n\n"
            "### Environmental Impact\n"
            "• Coal electricity emits $\\approx 0.713\\text{ to } 0.950\\text{ kg } CO_2e\\text{ / kWh}$.\n"
            "• Solar PV lifecycle emissions are under $0.040\\text{ kg } CO_2e\\text{ / kWh}$—a **$95\\%$ decarbonization dividend**!\n\n"
            "🇮🇳 *India's Target:* Reaching $500\\text{ GW}$ of non-fossil installed electricity capacity by 2030."
        ),
        "te": (
            "☀️ **పునరుత్పాదక శక్తి (Renewable Energy) అంటే ఏమిటి?**\n\n"
            "సూర్యకాంతి, గాలి, నీరు వంటి సహజ వనరుల నుండి నిరంతరం లభించే, కాలుష్యం కలిగించని శక్తిని **పునరుత్పాదక శక్తి** అంటారు.\n\n"
            "### ముఖ్య రకాలు:\n"
            "1. **సౌర శక్తి (Solar Power):** సూర్యరశ్మిని సోలార్ ప్యానెల్స్ ద్వారా విద్యుత్తుగా మార్చడం. మన దేశంలో సంవత్సరానికి 300 పైగా ఎండ రోజులు ఉంటాయి.\n"
            "2. **పవన శక్తి (Wind Energy):** పెద్ద విండ్‌మిల్లులు గాలి వీచడాన్ని ఉపయోగించి టర్బైన్లను తిప్పి విద్యుత్ ఉత్పత్తి చేస్తాయి.\n"
            "3. **జల విద్యుత్ (Hydro Power):** నదులు మరియు డ్యామ్‌ల నీటి ప్రవాహం ద్వారా విద్యుత్తును ఉత్పత్తి చేయడం.\n"
            "4. **బయోమాస్ & గ్రీన్ హైడ్రోజన్:** వ్యవసాయ వ్యర్థాల నుండి స్వచ్ఛమైన ఇంధనాన్ని తయారు చేయడం.\n\n"
            "బొగ్గు విద్యుత్ వల్ల వచ్చే కాలుష్యాన్ని 90% కంటే ఎక్కువ తగ్గించడానికి పునరుత్పాదక శక్తి అత్యవసరం!"
        ),
        "hi": (
            "☀️ **नवीकरणीय ऊर्जा (Renewable Energy) क्या है?**\n\n"
            "नवीकरणीय (अक्षय) ऊर्जा वह ऊर्जा है जो कभी न समाप्त होने वाले प्राकृतिक स्रोतों जैसे सूर्य, हवा, और पानी से प्राप्त होती है और पर्यावरण को नुकसान नहीं पहुँचाती।\n\n"
            "### इसके प्रमुख प्रकार:\n"
            "1. **सौर ऊर्जा (Solar Energy):** सोलर पैनल्स द्वारा सूर्य के प्रकाश को सीधे बिजली में बदलना।\n"
            "2. **पवन ऊर्जा (Wind Energy):** पवन चक्कियों (Wind Turbines) द्वारा तेज हवा की गतिज ऊर्जा से बिजली बनाना।\n"
            "3. **जल विद्युत (Hydroelectric Energy):** बांधों और बहते पानी के प्रवाह से टरबाइन चलाकर स्वच्छ बिजली प्राप्त करना।\n"
            "4. **बायोमास और हरित हाइड्रोजन:** कृषि अवशेषों और स्वच्छ जल इलेक्ट्रोलिसिस से प्रदूषण मुक्त ईंधन।\n\n"
            "कोयला बिजली की तुलना में सौर और पवन ऊर्जा से $90\\%$ से अधिक कम कार्बन उत्सर्जन होता है।"
        ),
    },

    "campus_sustainability": {
        "keywords": ["how can my college become sustainable", "sustainable campus", "green campus", "college sustainability", "కళాశాల పర్యావరణం", "క్యాంపస్ సుస్థిరత", "कॉलेज को सस्टेनेबल कैसे बनाएं", "ग्रीन कैंपस"],
        "en": (
            "🏫 **How Can a College Campus Become Sustainable?**\n\n"
            "Universities and colleges are living micro-cities where bold sustainability programs cultivate environmental leadership and yield deep institutional cost savings:\n\n"
            "### 1. Energy & Infrastructure Decarbonization\n"
            "• **Rooftop Solar Arrays:** Installing solar PV atop hostel and departmental rooftops to offset grid electricity ($0.713\\text{ kg/kWh}$). A $100\\text{ kWp}$ solar plant offsets over $110\\text{ tons of } CO_2$ annually.\n"
            "• **Smart Campus Lighting:** Sensor-activated LEDs in corridors, lecture halls, and libraries that automatically shut off when empty.\n"
            "• **BLDC & Energy-Star Appliances:** Upgrading hostel ceiling fans to 28W brushless DC (BLDC) motors and enforcing $24^\\circ\\text{C}$ setpoints on departmental AC units.\n\n"
            "### 2. Mobility & Low-Carbon Transit\n"
            "• **Pedestrian-First Core:** Banning private motor vehicles inside internal campus zones and providing electric buggies or shared campus bicycles.\n"
            "• **EV Charging Hubs:** Dedicated solar-powered charging stations for student and faculty electric two-wheelers.\n\n"
            "### 3. Food & Waste Circularity\n"
            "• **Mess Bio-Digesters:** Processing hostel food scraps through on-site anaerobic bio-gas plants to supply cooking fuel back to the mess kitchens.\n"
            "• **Zero Single-Use Plastic:** Enforcing reusable stainless steel utensils and water refill stations.\n"
            "• **Decentralized Composting:** Aerobic composting of fallen leaves and garden biomass for campus horticultural use.\n\n"
            "### 4. Student Gamification & Hostels Leaderboards\n"
            "• **Inter-Hostel Carbon Competitions:** Using this **CarbonCoach Leaderboard** to track per-capita emissions across hostels like *Hostel Krishna* and *Hostel Cauvery* with monthly green champion awards!"
        ),
        "te": (
            "🏫 **కళాశాల క్యాంపస్‌ను పర్యావరణ హితంగా (Sustainable) ఎలా మార్చవచ్చు?**\n\n"
            "మన కళాశాల మరియు హాస్టళ్లలో ఈ క్రింది మార్పుల ద్వారా హరిత క్యాంపస్‌గా మార్చవచ్చు:\n\n"
            "### 1. విద్యుత్ నిర్వహణ\n"
            "• హాస్టళ్లు మరియు డిపార్ట్‌మెంట్ భవనాల పైకప్పులపై **సోలార్ ప్యానెల్స్** ఏర్పాటు చేయడం.\n"
            "• సాధారణ లైట్ల బదులు సెన్సార్లతో కూడిన **LED లైట్లు** మరియు తక్కువ విద్యుత్ వినియోగించే **BLDC ఫ్యాన్లు** వాడడం.\n"
            "• తరగతి గదులు ఖాళీగా ఉన్నప్పుడు విద్యుత్ ఉపకరణాలు స్వయంచాలకంగా ఆపివేయడం.\n\n"
            "### 2. క్యాంపస్ ప్రయాణాలు\n"
            "• క్యాంపస్ లోపల పెట్రోల్ వాహనాలను పరిమితం చేసి **సైకిల్ షేరింగ్** లేదా ఎలక్ట్రిక్ వాహనాలను ప్రోత్సహించడం.\n\n"
            "### 3. ఆహారం మరియు వ్యర్థాల నిర్వహణ\n"
            "• హాస్టల్ మెస్ ఆహార వ్యర్థాలతో **బయోగ్యాస్ ప్లాంట్** ఏర్పాటు చేసి వంటకు ఉపయోగించడం.\n"
            "• ప్లాస్టిక్ వాడకాన్ని పూర్తిగా నిషేధించి స్టీల్ ప్లేట్లు, సీసాలు వాడడం.\n\n"
            "### 4. విద్యార్థుల పోటీలు\n"
            "• మన **CarbonCoach లీడర్‌బోర్డ్** ద్వారా హాస్టళ్ల మధ్య ఆరోగ్యకరమైన ఆదా పోటీలు నిర్వహించడం!"
        ),
        "hi": (
            "🏫 **कॉलेज कैंपस को हरित और सस्टेनेबल (Sustainable) कैसे बनाएं?**\n\n"
            "कॉलेज और विश्वविद्यालय स्तर पर निम्नलिखित कदमों से एक आदर्श ग्रीन कैंपस बनाया जा सकता है:\n\n"
            "### 1. स्वच्छ ऊर्जा और बिजली\n"
            "• सभी हॉस्टल और विभाग भवनों की छतों पर **रूफटॉप सोलर पैनल** लगाना।\n"
            "• ऊर्जा-कुशल **LED लाइट्स** और कम बिजली वाले **BLDC पंखे** लगाना।\n"
            "• खाली कक्षाओं और हॉस्टल कमरों में बिजली की बर्बादी रोकने के लिए जागरूकता अभियान।\n\n"
            "### 2. हरित परिवहन\n"
            "• कैंपस के अंदर निजी मोटर वाहनों को प्रतिबंधित कर **साइकिल शेयरिंग** और ईवी शटल को बढ़ावा देना।\n\n"
            "### 3. कचरा एवं खाद्य प्रबंधन\n"
            "• हॉस्टल मेस के जैविक कचरे से **बायोगैस संयंत्र** चलाना ताकि रसोई गैस बचाई जा सके।\n"
            "• सिंगल-यूज प्लास्टिक पर पूर्ण प्रतिबंध और जल पुनर्चक्रण (Water Recycling)।\n\n"
            "### 4. छात्र सहभागिता\n"
            "• हमारे **CarbonCoach लीडरबोर्ड** का उपयोग करके हॉस्टलों के बीच प्रति व्यक्ति उत्सर्जन कम करने की प्रतियोगिताएं आयोजित करना!"
        ),
    },
}


def find_knowledge_topic(message: str) -> Optional[Tuple[str, Dict[str, str]]]:
    """
    Scans a message for conceptual sustainability questions.
    Returns (topic_key, content_dict) if matched, else None.
    """
    msg_clean = message.lower().strip()

    # Check for direct or fuzzy keyword matches
    for topic_key, topic_data in KNOWLEDGE_TOPICS.items():
        for kw in topic_data["keywords"]:
            if kw in msg_clean:
                return topic_key, topic_data

    # Additional contextual triggers for general queries without calculation figures
    if any(q in msg_clean for q in ["what is carbon", "define carbon", "కార్బన్ అంటే", "కార్బన్ ఫుట్‌ప్రింట్", "కార్బన్ పాదముద్ర", "कार्बन क्या", "कार्बन फुटप्रिंट", "कार्बन पदचिह्न"]):
        return "carbon_footprint", KNOWLEDGE_TOPICS["carbon_footprint"]
    if any(q in msg_clean for q in ["climate change", "global warming", "जलवायु परिवर्तन", "వాతావరణ మార్పు", "భూతాపం", "గ్లోబల్ వార్మింగ్", "ग्लोबल वार्मिंग"]):
        return "climate_change", KNOWLEDGE_TOPICS["climate_change"]
    if any(q in msg_clean for q in ["why are carbon emissions harmful", "why is carbon bad", "హానికరం", "हानिकारक", "नुकसान"]):
        return "harmful_emissions", KNOWLEDGE_TOPICS["harmful_emissions"]
    if any(q in msg_clean for q in ["renewable", "solar energy", "wind energy", "పునరుత్పాదక", "సౌర", "सौर ऊर्जा", "नवीकरणीय"]):
        return "renewable_energy", KNOWLEDGE_TOPICS["renewable_energy"]
    if any(q in msg_clean for q in ["green campus", "sustainable college", "sustainable", "college", "కళాశాల", "క్యాంపస్", "హరిత", "कॉलेज", "कैंपस"]):
        return "campus_sustainability", KNOWLEDGE_TOPICS["campus_sustainability"]
    if any(q in msg_clean for q in ["reduce footprint", "reduce emissions", "how to reduce", "how can i reduce", "తగ్గించు", "ఎలా తగ్గించాలి", "कम करें", "कम करने के उपाय"]):
        return "reduce_footprint", KNOWLEDGE_TOPICS["reduce_footprint"]

    return None
