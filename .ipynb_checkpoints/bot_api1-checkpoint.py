{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\rasa_nlu\\training_data\\training_data.py:176: UserWarning: Intent 'askrating' has only 1 training examples! Minimum is 2, training may fail.\n",
      "  self.MIN_EXAMPLES_PER_INTENT))\n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\rasa_nlu\\training_data\\training_data.py:176: UserWarning: Intent 'interest3' has only 1 training examples! Minimum is 2, training may fail.\n",
      "  self.MIN_EXAMPLES_PER_INTENT))\n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\rasa_nlu\\training_data\\training_data.py:184: UserWarning: Entity 'interest1' has only 1 training examples! minimum is 2, training may fail.\n",
      "  self.MIN_EXAMPLES_PER_ENTITY))\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Fitting 2 folds for each of 6 candidates, totalling 12 fits\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\rasa_nlu\\extractors\\entity_synonyms.py:105: UserWarning: Found conflicting synonym definitions for 'london'. Overwriting target 'London' with 'london'. Check your training data and remove conflicting synonym definitions to prevent this from happening.\n",
      "  repr(replacement)))\n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\model_selection\\_split.py:651: Warning: The least populated class in y has only 1 members, which is too few. The minimum number of members in any class cannot be less than n_splits=2.\n",
      "  % (self.n_splits))\n",
      "[Parallel(n_jobs=1)]: Using backend SequentialBackend with 1 concurrent workers.\n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:1143: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no predicted samples.\n",
      "  \n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:1143: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no predicted samples.\n",
      "  \n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:1143: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no predicted samples.\n",
      "  \n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:1143: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no predicted samples.\n",
      "  \n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:1143: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no predicted samples.\n",
      "  \n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:1143: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no predicted samples.\n",
      "  \n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:1143: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no predicted samples.\n",
      "  \n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:1143: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no predicted samples.\n",
      "  \n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:1143: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no predicted samples.\n",
      "  \n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:1143: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no predicted samples.\n",
      "  \n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:1143: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no predicted samples.\n",
      "  \n",
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\sklearn\\metrics\\classification.py:1143: UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 in labels with no predicted samples.\n",
      "  \n",
      "[Parallel(n_jobs=1)]: Done  12 out of  12 | elapsed:    0.0s finished\n"
     ]
    }
   ],
   "source": [
    "import sqlite3\n",
    "from selenium import webdriver\n",
    "from selenium.webdriver.support.wait import WebDriverWait\n",
    "from selenium.webdriver.common.by import By\n",
    "import requests\n",
    "from bs4 import BeautifulSoup\n",
    "import json\n",
    "import math\n",
    "\n",
    "import time\n",
    "from selenium.webdriver.support import expected_conditions as EC\n",
    "\n",
    "\n",
    "import hug\n",
    "\n",
    "\n",
    "\n",
    "from selenium.webdriver.common.action_chains import ActionChains\n",
    "responses = [\"I'm sorry :( I couldn't find anything like that\",\"I'm sorry that I can't help you\", '{} is a great hotel!', '{} or {} would work!', '{} is one option, but I know others too :)']\n",
    "responsesdetail = [\"The hotel is {} ......\",\"This is some information about the hotel: {}.......\"]\n",
    "responsesrating = [\"The rating is {} \"]\n",
    "responsesprice = [\"The price is {} dollars\",\"It costs ${} per day \"]\n",
    "greet = [\"Hello\",\"Hi\",\"Hello! How can I help you\"]\n",
    "\n",
    "\n",
    "af = [\"Do you want to book it?\",\"Would you like me to give you the booking website?\"]\n",
    "           \n",
    "           \n",
    "def negated_ents(phrase, ent_vals,intent):\n",
    "    #ents = [e for e in ent_vals if e in phrase]\n",
    "    ents = [e for e in ent_vals ]\n",
    "    print(\"negastes\" + str(ents))\n",
    "    #ends = sorted([phrase.index(e) + len(e) for e in ents])\n",
    "    #start = 0\n",
    "    #chunks = []\n",
    "    #for end in ends:\n",
    "    #    chunks.append(phrase[start:end])\n",
    "    #    start = end\n",
    "    result = {}\n",
    "   # for chunk in chunks:\n",
    "    for ent in ents:\n",
    "  \n",
    "        if \"not\" in phrase or \"n't\" in phrase or intent == \"negate\":\n",
    "                    result[ent] = False\n",
    "        else:\n",
    "                    result[ent] = True\n",
    "    return result\n",
    "\n",
    "\n",
    "def interpret(message):\n",
    "    data = interpreter.parse(message)\n",
    "    if 'no' in message:\n",
    "        data[\"intent\"][\"name\"] = \"deny\"\n",
    "    return data\n",
    "\n",
    "#look for hotel from params\n",
    "def find_hotels(params, excluded, nparams):\n",
    "    #print(excluded)\n",
    "    query = 'SELECT * FROM hotel'\n",
    "    if len(params) > 0:\n",
    "        filters = [\"{}=?\".format(k) for k in params] + [\"{} <> ?\".format(k) for k in nparams] + [\"name!='?'\".format(k) for k in excluded] \n",
    "        query += \" WHERE \" + \" and \".join(filters)\n",
    "    t = tuple(params.values())+tuple(nparams.values())\n",
    "    \n",
    "    # open connection to DB\n",
    "    conn = sqlite3.connect('hoteltest1.db')\n",
    "    # create a cursor\n",
    "    c = conn.cursor()\n",
    "    c.execute(query, t)\n",
    "    return c.fetchall()\n",
    "\n",
    "infolist = [\"name\",\"city\",\"region\",\"country\",\"address\",\"description\",\"pricerange\",\"rating\",\"raterange\"]\n",
    "\n",
    "#look for extra hotel info from name\n",
    "def find_info(name,info):\n",
    " # open connection to DB\n",
    "    # open connection to DB\n",
    "    conn = sqlite3.connect('hoteltest1.db')\n",
    "    # create a cursor\n",
    "    c = conn.cursor()\n",
    "    index = 0\n",
    "    if info in infolist:\n",
    "        index = infolist.index(info)\n",
    "    t = str(name)\n",
    "    #print (t)\n",
    "    c.execute(\"SELECT \"+ info +\" FROM hotel WHERE name=:name\", {\"name\": t})\n",
    "    row = c.fetchall()\n",
    "    return row\n",
    "    \n",
    "        \n",
    "        \n",
    "# Import necessary modules\n",
    "from rasa_nlu.training_data import load_data\n",
    "from rasa_nlu.config import RasaNLUModelConfig\n",
    "from rasa_nlu.model import Trainer\n",
    "from rasa_nlu import config\n",
    "\n",
    "# Create a trainer that uses this config\n",
    "trainer = Trainer(config.load(r\"C:\\Users\\Shouyan\\Documents\\ai\\rasa_nlu-master\\sample_configs\\config_spacy.yml\"))\n",
    "\n",
    "# Load the training data\n",
    "training_data = load_data(r'C:\\Users\\Shouyan\\Documents\\ai\\train1.json')\n",
    "\n",
    "\n",
    "# Create an interpreter by training the model\n",
    "interpreter = trainer.train(training_data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [],
   "source": [
    "from selenium.webdriver.chrome.options import Options\n",
    "\n",
    "\n",
    "\n",
    "def find_website(name):\n",
    "    options = Options()\n",
    "    options.headless = True\n",
    "    #driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)\n",
    "    driver = webdriver.Chrome(r'C:\\Users\\Shouyan\\Documents\\ai\\chromedriver_win32 (1)\\chromedriver.exe',chrome_options=options) \n",
    "    driver.get('https://www.booking.com')\n",
    "    name = str(name)\n",
    "    driver.find_element_by_id('ss').send_keys(name)\n",
    "\n",
    "    driver.find_element_by_class_name(\"sb-searchbox__button\").click()\n",
    "\n",
    "    WebDriverWait(driver, 10)\n",
    "\n",
    "\n",
    "    headers = {\n",
    "        \"User-Agent\":\n",
    "    \"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36\"\n",
    "    }\n",
    "\n",
    "\n",
    "    url = driver.current_url\n",
    "    print(url)\n",
    "\n",
    "    return url\n",
    "    #return url\n",
    "\n",
    "#soup=BeautifulSoup(html,'html.parser')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [],
   "source": [
    "from itertools import chain\n",
    "from random import randint\n",
    "confirm = [\"OK,Have a great day, the url is {}. This may take some time, and the hotel might not be exist\"]\n",
    "\n",
    "\n",
    "def respond(message, params, suggestions, excluded,nparams,state,names1):\n",
    "    # Interpret the message\n",
    "    \n",
    "    if state == 0:\n",
    "        parse_data = interpret(message)\n",
    "        # Extract the intent\n",
    "        intent = parse_data[\"intent\"][\"name\"]\n",
    "        print(intent)\n",
    "        # Extract the entities\n",
    "        entities = parse_data[\"entities\"]\n",
    "        ent_vals = [e[\"value\"] for e in entities]\n",
    "        negated = negated_ents(message, ent_vals,intent)\n",
    "        # Add the suggestion to the excluded list if intent is \"deny\"\n",
    "        if intent == \"deny\" or \"not\" in message:\n",
    "            excluded.extend(suggestions)\n",
    "        # Fill the dictionary with entities\n",
    "       \n",
    "        for ent in entities:\n",
    "            if ent[\"value\"] in negated and negated[ent[\"value\"]] != True:\n",
    "\n",
    "               #params[ent[\"entity\"]] = str(ent[\"value\"])\n",
    "                nparams[ent[\"entity\"]] = str(ent[\"value\"])\n",
    "\n",
    "            else:\n",
    "                params[ent[\"entity\"]] = str(ent[\"value\"])\n",
    "        # Find matching hotels\n",
    "        results = [\n",
    "            r \n",
    "            for r in find_hotels(params, excluded,nparams) \n",
    "            if r[0] not in excluded\n",
    "        ]\n",
    "        # Extract the suggestions\n",
    "        names = [r[0] for r in results]\n",
    "        \n",
    "        if intent == \"affirm\":\n",
    "            \n",
    "            return greet[0].format(), params, suggestions, excluded, nparams,names,state,names1\n",
    "        \n",
    "        \n",
    "        n = min(len(results), 3)\n",
    "        suggestions = names[:2]\n",
    "        \n",
    "        #print(len(results))\n",
    "        \n",
    "        if len(results) == 0:\n",
    "            state = 0\n",
    "            \n",
    "        else:\n",
    "            state = 1\n",
    "            names1 = names[0]\n",
    "            \n",
    "            \n",
    "        if intent == \"greet\":\n",
    "            n = randint(0,3)\n",
    "            return greet[n].format(*info), params, suggestions, excluded, nparams,names,state,names1    \n",
    "            \n",
    "            \n",
    "        return responses[n].format(*names), params, suggestions, excluded, nparams,names,state,names1\n",
    "    \n",
    "    elif state == 2:\n",
    "        parse_data = interpret(message)\n",
    "        # Extract the intent\n",
    "        intent = parse_data[\"intent\"][\"name\"]\n",
    "        print(intent)\n",
    "        # Extract the entities\n",
    "        entities = parse_data[\"entities\"]\n",
    "        ent_vals = [e[\"value\"] for e in entities]\n",
    "        negated = negated_ents(message, ent_vals,intent)\n",
    "        # Add the suggestion to the excluded list if intent is \"deny\"\n",
    "        msg = message.lower()\n",
    "        if intent == \"affirm\":\n",
    "            \n",
    "            names = names1\n",
    "            state = 3\n",
    "            url = find_website(names)\n",
    "            return confirm[0].format(url), params, suggestions, excluded, nparams,names,state,names1\n",
    "        else:\n",
    "            names = names1\n",
    "            state = 1\n",
    "            return af[0].format() ,params,  suggestions, excluded, nparams,names,state,names1\n",
    "    \n",
    "    elif state == 1:\n",
    "        parse_data = interpret(message)\n",
    "        # Extract the intent\n",
    "        intent = parse_data[\"intent\"][\"name\"]\n",
    "        print(intent)\n",
    "        # Extract the entities\n",
    "        entities = parse_data[\"entities\"]\n",
    "        ent_vals = [e[\"value\"] for e in entities]\n",
    "        negated = negated_ents(message, ent_vals,intent)\n",
    "        print (negated)\n",
    "        # Add the suggestion to the excluded list if intent is \"deny\"\n",
    "        if intent == \"deny\" or \"not\" in message:\n",
    "            excluded.extend(suggestions)\n",
    "        # Fill the dictionary with entities\n",
    "        if intent == \"questingdetail\":\n",
    "            name = names1\n",
    "            #print(\"name is\" + name )\n",
    "            info = list(chain.from_iterable(find_info(name,\"description\")))\n",
    "            state = 1\n",
    "            names = names1\n",
    "            #print (info)\n",
    "            n = randint(0, 1)\n",
    "            return responsesdetail[n].format(*info), params, suggestions, excluded, nparams,names,state,names1\n",
    "        \n",
    "        if intent == \"askrating\":\n",
    "            name = names1\n",
    "            #print(\"name is\" + name )\n",
    "            info = list(chain.from_iterable(find_info(name,\"rating\")))\n",
    "            state = 1\n",
    "            names = names1\n",
    "            #print (info)\n",
    "    \n",
    "            return responsesrating[0].format(*info), params, suggestions, excluded, nparams,names,state,names1\n",
    "        \n",
    "        if intent == \"askprice\":\n",
    "            name = names1\n",
    "            #print(\"name is\" + name )\n",
    "            info = list(chain.from_iterable(find_info(name,\"price\")))\n",
    "            state = 1\n",
    "            names = names1\n",
    "            #print (info)\n",
    "            n = randint(0, 1)\n",
    "            return responsesprice[n].format(*info), params, suggestions, excluded, nparams,names,state,names1\n",
    "        \n",
    "        if intent == \"affirm\":\n",
    "            names = names1\n",
    "            #print(\"name is\" + name )\n",
    "            #info = list(chain.from_iterable(find_info(name,\"price\")))\n",
    "            #names = names1\n",
    "            #print (info)\n",
    "            n = randint(0, 1)\n",
    "            state = 2\n",
    "            print (state)\n",
    "            return af[n].format(), params, suggestions, excluded, nparams,names,state,names1\n",
    "        \n",
    "        if intent == \"greet\":\n",
    "            n = randint(0,3)\n",
    "            return greet[n].format(), params, suggestions, excluded, nparams,names,state,names1\n",
    "        \n",
    "        \n",
    "        for ent in entities:\n",
    "            if ent[\"value\"] in negated and negated[ent[\"value\"]] != True:\n",
    "\n",
    "               #params[ent[\"entity\"]] = str(ent[\"value\"])\n",
    "                nparams[ent[\"entity\"]] = str(ent[\"value\"])\n",
    "\n",
    "            else:\n",
    "                params[ent[\"entity\"]] = str(ent[\"value\"])\n",
    "        # Find matching hotels\n",
    "        results = [\n",
    "            r \n",
    "            for r in find_hotels(params, excluded,nparams) \n",
    "            if r[0] not in excluded\n",
    "        ]\n",
    "        # Extract the suggestions\n",
    "        names = [r[0] for r in results]\n",
    "        names1 = names[0]\n",
    "        n = min(len(results), 3)\n",
    "        suggestions = names[:2]\n",
    "        if n == 0:\n",
    "            state = 0\n",
    "        else:\n",
    "            state = 1\n",
    "            \n",
    "        \n",
    "        return responses[n].format(*names), params, suggestions, excluded, nparams,names,state,names1\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "USER : I'm looking for a hotel near chicago downtown\n",
      "hotel_search\n",
      "negastes['Downtown']\n",
      "BOT : Gold Coast 26B or Oakwood 200 Squared would work!\n",
      "USER : How much is it\n",
      "askprice\n",
      "negastes[]\n",
      "{}\n",
      "BOT : It costs $351 per day \n",
      "USER : it is too expensive\n",
      "negate\n",
      "negastes['HI']\n",
      "{'HI': False}\n",
      "BOT : Oakwood 200 Squared or Dewitt Hotel and Suites would work!\n",
      "USER : How much is it\n",
      "askprice\n",
      "negastes[]\n",
      "{}\n",
      "BOT : It costs $191 per day \n",
      "USER : I want a place to live near chicago downtown\n",
      "hotel_search\n",
      "negastes['Downtown']\n",
      "{'Downtown': True}\n",
      "BOT : Oakwood 200 Squared or Dewitt Hotel and Suites would work!\n",
      "USER : is it good\n",
      "askprice\n",
      "negastes[]\n",
      "{}\n",
      "BOT : It costs $191 per day \n",
      "USER : can you tell me more about it\n",
      "questingdetail\n",
      "negastes[]\n",
      "{}\n",
      "BOT : This is some information about the hotel: Located downtown in the Chicago Loop, Oakwood 200 Squared offers an indoor pool and a rooftop sundeck with a fire pit and city views........\n",
      "USER : Sounds good\n",
      "affirm\n",
      "negastes[]\n",
      "{}\n",
      "2\n",
      "BOT : Do you want to book it?\n",
      "USER : Ok\n",
      "affirm\n",
      "negastes[]\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Shouyan\\Anaconda3\\lib\\site-packages\\ipykernel_launcher.py:9: DeprecationWarning: use options instead of chrome_options\n",
      "  if __name__ == '__main__':\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "https://www.booking.com/index.en-gb.html?;errorv_class_interval=1;errorv_error_url=https%253A%252F%252Fwww.booking.com%252Findex.en-gb.html%253Flabel%253Dgen173nr-1FCAEoggI46AdIM1gEaJMCiAEBmAEJuAEKyAEF2AEB6AEB-AELiAIBqAIDuAL50IbvBcACAQ%253Bsid%253D3e7ff7615a5f58a56f960738c8ddef4c%253Bsb_price_type%253Dtotal%2526%253B;errorv_from_sf=1;errorv_group_adults=2;errorv_label_click=undef;errorv_no_rooms=1;errorv_room1=A%252CA;errorv_sb_price_type=total;errorv_shw_aparth=1;errorv_src=index;errorv_src_elem=sb;errorv_ss=Oakwood%2520200%2520Squared;errorv_ssb=empty;errorv_top_ufis=1;label=gen173nr-1FCAEoggI46AdIM1gEaJMCiAEBmAEJuAEKyAEF2AEB6AEB-AELiAIBqAIDuAL50IbvBcACAQ;sb_price_type=total;sid=3e7ff7615a5f58a56f960738c8ddef4c\n",
      "BOT : OK,Have a great day, the url is https://www.booking.com/index.en-gb.html?;errorv_class_interval=1;errorv_error_url=https%253A%252F%252Fwww.booking.com%252Findex.en-gb.html%253Flabel%253Dgen173nr-1FCAEoggI46AdIM1gEaJMCiAEBmAEJuAEKyAEF2AEB6AEB-AELiAIBqAIDuAL50IbvBcACAQ%253Bsid%253D3e7ff7615a5f58a56f960738c8ddef4c%253Bsb_price_type%253Dtotal%2526%253B;errorv_from_sf=1;errorv_group_adults=2;errorv_label_click=undef;errorv_no_rooms=1;errorv_room1=A%252CA;errorv_sb_price_type=total;errorv_shw_aparth=1;errorv_src=index;errorv_src_elem=sb;errorv_ss=Oakwood%2520200%2520Squared;errorv_ssb=empty;errorv_top_ufis=1;label=gen173nr-1FCAEoggI46AdIM1gEaJMCiAEBmAEJuAEKyAEF2AEB6AEB-AELiAIBqAIDuAL50IbvBcACAQ;sb_price_type=total;sid=3e7ff7615a5f58a56f960738c8ddef4c. This may take some time, and the hotel might not be exist\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "'BOT : OK,Have a great day, the url is https://www.booking.com/index.en-gb.html?;errorv_class_interval=1;errorv_error_url=https%253A%252F%252Fwww.booking.com%252Findex.en-gb.html%253Flabel%253Dgen173nr-1FCAEoggI46AdIM1gEaJMCiAEBmAEJuAEKyAEF2AEB6AEB-AELiAIBqAIDuAL50IbvBcACAQ%253Bsid%253D3e7ff7615a5f58a56f960738c8ddef4c%253Bsb_price_type%253Dtotal%2526%253B;errorv_from_sf=1;errorv_group_adults=2;errorv_label_click=undef;errorv_no_rooms=1;errorv_room1=A%252CA;errorv_sb_price_type=total;errorv_shw_aparth=1;errorv_src=index;errorv_src_elem=sb;errorv_ss=Oakwood%2520200%2520Squared;errorv_ssb=empty;errorv_top_ufis=1;label=gen173nr-1FCAEoggI46AdIM1gEaJMCiAEBmAEJuAEKyAEF2AEB6AEB-AELiAIBqAIDuAL50IbvBcACAQ;sb_price_type=total;sid=3e7ff7615a5f58a56f960738c8ddef4c. This may take some time, and the hotel might not be exist'"
      ]
     },
     "execution_count": 33,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "state = 0\n",
    "params, suggestions, excluded,nparams,names1 = {}, [], [],{},[]\n",
    "\n",
    "def send(message):\n",
    "    \n",
    "    global params,suggestions,excluded,nparams,names1 \n",
    "    global state\n",
    "    \n",
    "   \n",
    "   \n",
    "    print(\"USER : {}\".format(message))\n",
    "    \n",
    "    response, params, suggestions, excluded,nparams,names,state,names1 = respond(message, params, suggestions, excluded, nparams,state,names1)\n",
    "    \n",
    "    print(\"BOT : {}\".format(response))\n",
    "    return \"BOT : {}\".format(response)\n",
    "    #return response\n",
    "    #return response, params, suggestions, excluded,nparams,names,state,names1\n",
    "\n",
    "# Send the messages\n",
    "mes = [\"I'm looking for a hotel near chicago downtown\",\"How much is it\",\"it is too expensive\",\"How much is it\",\"I want a place to live near chicago downtown\",\"is it good\" ,\"can you tell me more about it\",\"Sounds good\",\"Ok\"]\n",
    "\n",
    "send(mes[0])\n",
    "send(mes[1])\n",
    "send(mes[2])\n",
    "send(mes[3])\n",
    "send(mes[4])\n",
    "send(mes[5])\n",
    "send(mes[6])\n",
    "send(mes[7])\n",
    "send(mes[8])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'chatterbot_corpus'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-30-94fee5512e82>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mChatBot\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      2\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mtrainers\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mChatterBotCorpusTrainer\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      3\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      4\u001b[0m \u001b[1;33m@\u001b[0m\u001b[0mhug\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mget\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      5\u001b[0m \u001b[1;32mdef\u001b[0m \u001b[0mget_response\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0muser_input\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\chatterbot\\__init__.py\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m      2\u001b[0m \u001b[0mChatterBot\u001b[0m \u001b[1;32mis\u001b[0m \u001b[0ma\u001b[0m \u001b[0mmachine\u001b[0m \u001b[0mlearning\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mconversational\u001b[0m \u001b[0mdialog\u001b[0m \u001b[0mengine\u001b[0m\u001b[1;33m.\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      3\u001b[0m \"\"\"\n\u001b[1;32m----> 4\u001b[1;33m \u001b[1;32mfrom\u001b[0m \u001b[1;33m.\u001b[0m\u001b[0mchatterbot\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mChatBot\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      5\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      6\u001b[0m \u001b[0m__version__\u001b[0m \u001b[1;33m=\u001b[0m \u001b[1;34m'1.0.5'\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\chatterbot\\chatterbot.py\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m      1\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mlogging\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m----> 2\u001b[1;33m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mstorage\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mStorageAdapter\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      3\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mlogic\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mLogicAdapter\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      4\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0msearch\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mIndexedTextSearch\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      5\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mutils\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\chatterbot\\storage\\__init__.py\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[1;32m----> 1\u001b[1;33m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mstorage\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mstorage_adapter\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mStorageAdapter\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      2\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mstorage\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mdjango_storage\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mDjangoStorageAdapter\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      3\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mstorage\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mmongodb\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mMongoDatabaseAdapter\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      4\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mstorage\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0msql_storage\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mSQLStorageAdapter\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      5\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\chatterbot\\storage\\storage_adapter.py\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m      1\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mlogging\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      2\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mlanguages\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m----> 3\u001b[1;33m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mtagging\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mPosHypernymTagger\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      4\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      5\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\chatterbot\\tagging.py\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m      2\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mlanguages\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      3\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mutils\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m----> 4\u001b[1;33m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mtokenizers\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mget_sentence_tokenizer\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      5\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mnltk\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mpos_tag\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      6\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mnltk\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mcorpus\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mwordnet\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mstopwords\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\chatterbot\\tokenizers.py\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m      2\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mnltk\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mtokenize\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mpunkt\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mPunktSentenceTokenizer\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mPunktTrainer\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      3\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mnltk\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mtokenize\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0m_treebank_word_tokenizer\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m----> 4\u001b[1;33m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mcorpus\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mload_corpus\u001b[0m\u001b[1;33m,\u001b[0m \u001b[0mlist_corpus_files\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      5\u001b[0m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mlanguages\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      6\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m~\\Anaconda3\\lib\\site-packages\\chatterbot\\corpus.py\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m      3\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mglob\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      4\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0myaml\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m----> 5\u001b[1;33m \u001b[1;32mfrom\u001b[0m \u001b[0mchatterbot_corpus\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mcorpus\u001b[0m \u001b[1;32mimport\u001b[0m \u001b[0mDATA_DIRECTORY\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m      6\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m      7\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'chatterbot_corpus'"
     ]
    }
   ],
   "source": [
    "\"\"\"\n",
    "from chatterbot import ChatBot\n",
    "from chatterbot.trainers import ChatterBotCorpusTrainer\n",
    "\n",
    "@hug.get()\n",
    "def get_response(user_input):\n",
    "    response = send(user_input).text\n",
    "    return {\"response\":response}\n",
    "\"\"\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "itchat has already logged in.\n",
      "Start auto replying.\n"
     ]
    }
   ],
   "source": [
    "import itchat\n",
    "\n",
    "@itchat.msg_register(itchat.content.TEXT)\n",
    "def text_reply(msg):\n",
    "    return send(msg)\n",
    "\n",
    "itchat.auto_login(True, enableCmdQR=True)\n",
    "itchat.run()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<ItchatReturnValue: {'BaseResponse': {'Ret': 1, 'ErrMsg': '', 'RawMsg': ''}, 'MsgID': '', 'LocalID': ''}>"
      ]
     },
     "execution_count": 40,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "itchat.send('Hello, filehelper', toUserName='filehelper')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}