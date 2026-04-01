# subtitler

Listens to your computer's microphone,
transcribes it to text,
translates it from English to Portuguese,
by default,
and displays subtitles as a screen overlay - live.

Feels like magic... And fun, and silly! Maybe useful, you never know.


## Requirements

On *works for me* after fiddling with it for a coupe of hours basis. 🤷🏻‍♂️

* A computer running macOS (the UI overlay needs tweaks for other plaforms).
* Internet connectivity.
* An API key from [Deepgram](https://deepgram.com/) for speech to text. [see note 1]
* An API key from [DeepL](https://www.deepl.com/) for translation. [see note 2]

Notes, as of this writing:

1. There's a free USD 200.00 credit in a *pay as you go* model;
   enough for 400+ hours of speech to text with the most expensive model.
2. The free version allows for 50k characeters/month.


## Running

* Set the `DEEPGRAM_API_KEY` environment variable.
* Set the `DEEPL_API_KEY` environment variable.
* `uv run subtitler`


## Tweaking 

* Play with the `src/subtitler/config.py` module.
* Things you can easily change:
  * Spoken language.
  * Subtitle language.
  * Font family and size.


## The background story

On April 1st, 2026, a person, **isi**, joined the [Python Lisbon Meetup](https://python-lisbon-meetup.github.io/) Discord channel and asked:

> Hello, it’s a pleasure to meet you all.
> I’ve just started learning Python and noticed that you organise meet-ups
> on this programming language.
> Do you think I’ll be able to keep up, even though I’m a beginner,
> or are the topics too advanced? (I only speak Spanish or Portuguese )

As an organizer, I promptly responded:

> If you’re interested in Python you will be welcome…
> Join us tomorrow and come say hi.
> As for languages, we speak all of them… But mostly Python! 😊

A few minutes later, **Rodrigo**, a co-organizer, noted, in private,
that I didn't mention that talks tend to be in English.

And then, in a friendly tone, he also responded to **isi**, in Portuguese:

> Todos são bem-vindos, independentemente do nível de experiência . 😄
> As palestras costumam ser dadas em inglês por causa do número de estrangeiros
> que frequentam os nossos encontros.
> Como disseste que só falas português ou espanhol,
> mas escreveste a mensagem em inglês,
> fiquei na dúvida se isto podia ser um problema ou não :/

To which, I replied, sharing a thought:

> (pensamento: conseguiremos ter palestras em inglês, por exemplo,
> legendadas em português?!… graçola ou pensamento sério?) 🤔

Then **Marco** provocatively (in a funny way) replied:

> É só arranjar um estenografo

My last message, to **Marco**, was:

> …ah, “só” isso. Resolvido, então! 🤷🏻‍♂️

## Development Notes (for those concerned about AI)

* I chatted a bit with Google Gemini in exploring ideas and identifying
  speech to text and translation services I could easily use from Python.

* I chatted a bit with Claude via [llm](https://llm.datasette.io/en/stable/),
  a CLI tool I use all the time, to get my AsyncIO skills up to speed
  (hadn't touched async code in a while).

* Having prior experience with [sounddevice](https://pypi.org/project/sounddevice/)
  and with `tkinter` as a tool to create transparent text overlays,
  the remaining code was mostly adapted from Deepgram/DeepL examples and docs.

* All of the code was written by myself, mostly as an experiment,
  and of course as a fun thing to bring to our montly meetup, tomorrow,
  April, 2nd, 2026.


## License

The MIT License (MIT)

Copyright © 2026 Tiago Montes

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
