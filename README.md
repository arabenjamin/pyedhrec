# Ara's Awesome Commander Agent 
## Overview

My Buddy wants a widget that tells him how unique his commander deck is commpared to all of the other decks for that commander. I need a project to learn Ai/Ml. The aim from here is to build an AI agent that will do the needfull.

I forked this repo from some [guy](https://github.com/stainedhat/pyedhrec) so we could ... commandeer some information we needed.  


So far, I have collected the info we need to get started, and I have created a docker compose that will run neo4j, ollama, and n8n. 

Using this hacky-ass python script, and [mtgjson](https://mtgjson.com/) as data sources, I'm going to build an agent that:

* Evalutes all decks for a given commander, including price points for the deck
* Evaluates your deck against all other decks built with that commander
* Offer suggestions on how to best edit your deck, including tiered priced suggestions. 



