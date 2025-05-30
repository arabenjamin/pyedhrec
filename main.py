import logging
import requests


import duckdb

from edhrec import EDHRec





def store_all_decks(decks:dict, my_decklist:list, onlyOne:bool=False):

    print(f"My Deck has {len(my_decklist)} cards")

    logger.info(f"Storing Deck List ({len(my_decklist)} cards ) in my decklist table")
    with duckdb.connect() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS my_decklist (name VARCHAR, usedIn INT DEFAULT 0)")
        for card in my_decklist:
            conn.execute("INSERT INTO my_decklist VALUES (?, ?)", (card, 0))

        # Query the table to verify the data
        result = conn.execute("SELECT count(name) FROM my_decklist").fetchall()
        logger.info(f"My Deck List has {result[0][0]} cards")
        print(f"My Deck List has {result[0][0]} cards in duckdb")

        # Get the deck hash for the url endpoint
        if onlyOne:
            urlhash = decks["table"][0]['urlhash']
            logger.info(f"Getting deck for deck hash {urlhash}")
            
            deck_data = edhrec.get_commander_deck_list(urlhash)
            log_msg = f"Deck {urlhash} has {len(deck_data['cards'])} cards"
            logger.info(log_msg)
            print(log_msg)
            logger.info(f"Deck Cards {deck_data['cards']}")


            with duckdb.connect() as conn:

                conn.execute(f"CREATE TABLE IF NOT EXISTS {urlhash.replace("-", "_")} (name VARCHAR, inMyDeck BOOLEAN)")
                
                for card in deck_data['cards']:
                        inMyDeck = False
                        if card in my_decklist:
                            inMyDeck = True
                        conn.execute(f"INSERT INTO {urlhash.replace("-", "_")} VALUES (?, ?) ",(card, inMyDeck,)  )
                
                # Query the table to verify the data
                result = conn.execute(f"SELECT count(inMyDeck) FROM {urlhash.replace("-", "_")} WHERE inMyDeck IS True").fetchall()
                

                
                result_msg = f"Deck {urlhash} has {result[0][0]} cards that are in my deck"
                print(result_msg)
                logger.info(result_msg)

                logger.info(f"Deck {urlhash} stored in DuckDB")

                percentage = (result[0][0] / len(deck_data['cards'])) * 100

                logger.info(f"Deck {urlhash} has {percentage}% of my deck")
                print(f"Deck {urlhash} has {percentage}% of my deck")
                
                return None
        else:

            for deck in decks["table"]:

                urlhash = deck['urlhash']
                logger.info(f"Getting deck list for deck hash {urlhash}")
                deck_data = edhrec.get_commander_deck_list(urlhash)
                
                logger.info(f"Deck Cards length {len(deck_data['cards'])}")
                logger.info(f"Deck Cards {deck_data['cards']}")
                print(f"Storing deck {urlhash} with {len(deck_data['cards'])} cards")
                conn.execute(f"CREATE TABLE IF NOT EXISTS {str(urlhash.replace("-", "_").strip())} (name VARCHAR, inMyDeck BOOLEAN)")
                for card in deck_data['cards']:
                    inMyDeck = False
                    if card in my_decklist:
                        inMyDeck = True
                        conn.execute(f"UPDATE my_decklist SET usedIn = usedIn+1 WHERE name = (?)", (card,))

                    conn.execute(f"INSERT INTO {urlhash.replace("-", "_")} VALUES (?, ?) ",(card, inMyDeck,)  )
            
                result = conn.execute(f"SELECT count(inMyDeck) FROM {urlhash.replace("-", "_")} WHERE inMyDeck IS True").fetchall()
                # Query the table to verify the data
                #result = conn.execute(f"SELECT name FROM {urlhash}").fetchall()
                #print(result)
                result_msg = f"Deck {urlhash} has {result[0][0]} cards that are in my deck"
                print(result_msg)
                logger.info(result_msg)
                percentage = (result[0][0] / len(deck_data['cards'])) * 100
                logger.info(f"Deck {urlhash} has {percentage}% of my deck")
                print(f"Deck {urlhash} has {percentage}% of my deck")
                logging.info(f"Deck {urlhash} stored in DuckDB")
            


            result = conn.execute("SELECT name, usedIn FROM my_decklist").fetchall()
            for card, usedIn in result:
                logger.info(f"Card {card} is used in {usedIn} decks")
                print(f"Card {card} is used in {usedIn} decks")
            


            return None
    



def get_my_decklist() -> list:
    """
    Get My Deck list from Moxfield
    """
    with open("hosts-of-mordor.txt", "r") as f:
        cards = f.readlines()
        decklist = []
        for card in cards:
            try:
                card = card.split(" ")[1:]
                card = " ".join(card)
                card = card.replace("’", "'")
                card = card.replace("\n", "")
                decklist.append(card)

            except IndexError:
                logger.error(f"Error parsing card {card}")
                continue

        logger.info(f"MY Deck list length {len(decklist)}")
        logger.info(f"My Deck list {decklist}")
        return decklist
    
    return




if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="edhrec_data.log",
        level=logging.INFO
    )

    logger.info("Starting Deck Analisys")
    edhrec = EDHRec()


    # NOTE/TODO: We're setting the commander and deck list here, 
    # Ideally we should be getting that more dynamicly 

    # TODO: Get my deck list
    commander = "Saruman, the White Hand"
    my_decklist = get_my_decklist()
    logger.info(f"My commander {commander} has {len(my_decklist)} cards")
    

    # Get the recorded decks for this commander
    decks = edhrec.get_commander_decks(commander)
    logger.info(f"We have {len(decks['table'])} decks")
    #logger.info(f"Deck Keys: {decks['table'][0].keys()}")

    # store all decks or just the first one
    store_all_decks(decks, my_decklist, onlyOne=False)
    # TODO: Stick ALL into db



        




    
    

    



