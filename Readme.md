# F1 FIA Document Parser

This project is a Python-based tool for retrieving and processing FIA Formula One World Championship documents and its related information. It can download PDFs, process event notes, and handle penalties for a given season and Grand Prix (GP).

This stems from a separate project where I encountered the need to understand which compounds were associated with the SOFT, MEDIUM, HARD tyre types returned from the Fastf1 API (https://github.com/theOehrly/Fast-F1). I decided to use LLMs in order to be able to generalize and avoid having to parse multiple changing document types. I have found an effort to take this information to a proper API (https://github.com/theOehrly/Fast-F1/issues/332) for which maybe this code might help with.

This is as well a good use case for Retrieval-Augmented Generation (RAG) and Language Models (LLMs) to extract and enrich data from these documents.

The code can be easily extended to deal with documents from other competitions, for such feel free to check the license in order to extend it.

## Warning
In order to provide a generalist approach, I am using LLMs to perform information retrieval (RAG) so the extracted information is not deterministic. To the best of my time, I have been able to validate its accuracy however it is recommended you put some validations before using the data returned.

## Installation

To install the F1 FIA Document Parser, you will need Python 3.6 or later. Clone the repository and install the required packages:

```
bash
git clone https://github.com/marcll/f1-fia-document-parser.git
cd f1-fia-document-parser
pip install -r requirements.txt
```

For running `--event-notes` or `--penalty-notes` parsing you will be required to have an OpenAI API key. For this, create an .env file within the root folder with the `OPENAI_API_KEY`.

## Usage

The F1 FIA Document Parser can be run from the command line with various options:

- `--force`: Force re-download of PDFs
- `--season`: Process documents for a given season
- `--gp`: Process documents for a given GP
- `--event-notes`: Process event notes for the given season and GP
- `--penalty-notes`: Process penalties for the given season and GP (not yet implemented)
- `--verbosity`: Set the verbosity level of the program ('DEBUG', 'WARNING', 'DEFAULT')


Example usage:


```python main.py --season 2021 --gp "British Grand Prix" --event-notes --verbosity DEBUG```


This will process the event notes for the 2021 British Grand Prix with debug verbosity.


```python main.py --season 2022 --gp "British Grand Prix" --event-notes --verbosity Warning```


This will download all the F1 FIA Documents for the 2022 British Grand Prix with warning verbosity.

## Running

To run the F1 FIA Document Parser, navigate to the project directory and run the `main.py` script.

## License

This project is licensed under the terms of the MIT license. For more details, see the LICENSE file in the project's root directory.



## Comparing models outputs 

gpt-3.5-turbo cost round ~$0.018 per question

```
========================================
Summarized Infringiments for Canadian Grand Prix in season 2024.
========================================


Which drivers and cars had received penalty or fine decision? Check Infringement, Summons and Decisions documents
-----------------------------------------------------------------------------------------------------------------
1. Driver 11 - Sergio Perez from Oracle Red Bull Racing received a penalty for breaching Article 26.10 of the FIA Formula One Sporting Regulations, resulting in a €25,000 fine and a three-grid position drop for the next race.

2. Driver 16 - Charles Leclerc from Scuderia Ferrari received a fine of €5,000 for using Intermediate tires when the track was not declared wet.

3. Driver 22 - Yuki Tsunoda from Visa Cash App RB F1 Team was fined €10,000 for late attendance during the National Anthem.

4. Driver 3 - Daniel Ricciardo from Visa Cash App RB F1 Team received a 5-second time penalty for a false start.

5. Driver 77 - Valtteri Bottas from Stake F1 Team Kick Sauber was required to start the Race from the pit lane for using excessive Power Unit elements and changing the rear wing specification under Parc Ferme.

6. There was no penalty or fine decision for Driver 4 - Lando Norris from McLaren Formula 1 Team based on the reviewed documents.
```

gpt-4o cost round ~$0.067 per question
```
Which drivers and cars had received penalty or fine decision? Check Infringement, Summons and Decisions documents
-----------------------------------------------------------------------------------------------------------------
Based on the provided context, the following drivers and cars received penalties or fines:

1. **Sergio Perez (Car 11, Oracle Red Bull Racing)**
   - **Infringement**: Breach of Article 26.10 of the FIA Formula One Sporting Regulations.
   - **Decision**: Fined €25,000 and a drop of three grid positions for the next race.
   - **Reason**: Continued on track with a significantly damaged car after making contact with the barriers, losing several carbon fiber parts.

2. **Charles Leclerc (Car 16, Scuderia Ferrari)**
   - **Infringement**: Breach of Article 30.5 l) of the FIA Formula One Sporting Regulations (Using Intermediate tyres when the track was not declared wet).
   - **Decision**: The competitor (Scuderia Ferrari) is fined €5,000.
   - **Reason**: Used intermediate tires on a non-wet track and returned to the pits after one lap.

3. **Yuki Tsunoda (Car 22, Visa Cash App RB F1 Team)**
   - **Infringement**: Breach of Article 19.4 b) of the FIA Formula One Sporting Regulations (Late for National Anthem).
   - **Decision**: The competitor (Visa Cash App RB F1 Team) is fined €10,000.
   - **Reason**: Late attendance of the National Anthem due to a failure in communication from the team.

4. **Zhou Guanyu (Car 24, Stake F1 Team Kick Sauber)**
   - **Infringement**: Breach of Article 40.3 of the FIA Formula One Sporting Regulations (Changing rear wing specification under Parc Ferme).
   - **Decision**: Required to start the race from the pit lane.
   - **Reason**: Changed the rear wing assembly to a different specification under Parc Ferme.

5. **Valtteri Bottas (Car 77, Stake F1 Team Kick Sauber)**
   - **Infringement**: Breach of Articles 28.2 and 40.3 of the FIA Formula One Sporting Regulations (Use of Power Unit elements in excess and changing rear wing specification under Parc Ferme).
   - **Decision**: Required to start the race from the pit lane.
   - **Reason**: Used Power Unit elements in excess of the permitted number and changed the rear wing assembly to a different specification under Parc Ferme.

6. **Daniel Ricciardo (Car 3, Visa Cash App RB F1 Team)**
   - **Infringement**: Breach of Article 48.1 of the FIA Formula One Sporting Regulations (False Start).
   - **Decision**: 5 second time penalty.
   - **Reason**: Car moved after the 4-second light was illuminated and before the start signal was given.

These penalties and fines were imposed for various breaches of the FIA Formula One Sporting Regulations and the International Sporting Code.
```


## Example output 

Running the following command, using the gpt4-o OpenAI model 

```
python main.py --season 2024 --gp "Canadian Grand Prix"  --event-notes --penalty-notes
```

Would output the following summarized information


```
========================================
Summarized Infringiments for Canadian Grand Prix in season 2024.
========================================


Which drivers and cars had received penalty or fine decision? Check Infringement, Summons and Decisions documents
-----------------------------------------------------------------------------------------------------------------
Based on the provided documents, the following drivers and cars received penalties or fines:

1. **Sergio Perez (Car No. 11, Oracle Red Bull Racing)**:
   - **Infringement**: Breach of Article 26.10 of the FIA Formula One Sporting Regulations.
   - **Decision**: The competitor (Oracle Red Bull Racing) is fined €25,000. Additionally, a drop of three grid positions for the next race in which the driver participates.
   - **Reason**: Continued on track with a significantly damaged car after making contact with barriers, losing several carbon fiber parts on the way back to the pits.

2. **Charles Leclerc (Car No. 16, Scuderia Ferrari)**:
   - **Infringement**: Breach of Article 30.5 l) of the FIA Formula One Sporting Regulations.
   - **Decision**: The competitor (Scuderia Ferrari) is fined €5,000.
   - **Reason**: Using intermediate tires when the track was not declared wet.

3. **Yuki Tsunoda (Car No. 22, Visa Cash App RB F1 Team)**:
   - **Infringement**: Breach of Article 19.4 b) of the FIA Formula One Sporting Regulations.
   - **Decision**: The competitor (Visa Cash App RB F1 Team) is fined €10,000.
   - **Reason**: Late attendance of the National Anthem.

4. **Zhou Guanyu (Car No. 24, Stake F1 Team Kick Sauber)**:
   - **Infringement**: Breach of Article 40.3 of the FIA Formula One Sporting Regulations.
   - **Decision**: Required to start the race from the pit lane.
   - **Reason**: The rear wing specification was changed while under Parc Ferme.

5. **Valtteri Bottas (Car No. 77, Stake F1 Team Kick Sauber)**:
   - **Infringement**: Breach of Articles 28.2 and 40.3 of the FIA Formula One Sporting Regulations.
   - **Decision**: Required to start the race from the pit lane.
   - **Reason**: Use of power unit elements in excess of the permitted number and changing the rear wing assembly to a different specification under Parc Ferme.

6. **Daniel Ricciardo (Car No. 3, Visa Cash App RB F1 Team)**:
   - **Infringement**: Breach of Article 48.1 of the FIA Formula One Sporting Regulations.
   - **Decision**: 5-second time penalty.
   - **Reason**: False start.

These decisions were made by the Stewards based on the relevant regulations, guidelines, and evidence presented.



Which drivers/cars had received no further actions
--------------------------------------------------
The following drivers/cars received no further action:

1. **George Russell (Car 63)** - Incident between Cars 81 (Oscar Piastri) and 63 in Turn 13 and 14 during the race. The Stewards determined that no driver was wholly or predominantly at fault.

2. **Lando Norris (Car 4)** - Alleged leaving the track and gaining an advantage in Turn 1 during the race. The Stewards determined that Car 4 did not gain any lasting advantage.

3. **Max Verstappen (Car 1)** - Alleged breach of Article 34.8 of the Formula One Sporting Regulations and Appendix L, Chapter IV, Article 5b of the International Sporting Code during qualifying. The Stewards found that the requirements were fulfilled and took no further action.

4. **Oscar Piastri (Car 81)** - Alleged failure to follow the Race Director’s Event Notes regarding the escape road instructions at Turn 14 during Practice 3. The Stewards determined that he rejoined in a safe manner and no further action was warranted.

5. **Lando Norris (Car 4)** - Alleged failure to follow the Race Director’s Event Notes regarding the escape road instructions at Turn 14 during Practice 2. The Stewards determined that no infringement occurred.



What penalties are meant to be served on next race?
---------------------------------------------------
The following penalties are meant to be served in the next race:

1. **Sergio Perez (Oracle Red Bull Racing)**:
   - A drop of three grid positions for the next race in which he participates, due to continuing to drive with an unsafe car after significantly damaging the rear wing.

2. **Zhou Guanyu (Stake F1 Team Kick Sauber)**:
   - Required to start the next race from the pit lane, due to changing the rear wing assembly to a different specification while under Parc Ferme.

3. **Valtteri Bottas (Stake F1 Team Kick Sauber)**:
   - Required to start the next race from the pit lane, due to using Power Unit elements in excess of the permitted number and changing the rear wing assembly to a different specification while under Parc Ferme.

These penalties are specified in the documents related to the 2024 Canadian Grand Prix.
```
