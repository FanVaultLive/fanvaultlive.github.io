# FanVault.Live — an Open Web Publishing Library
k-pop n
### Cards. Stories. Collections. Creative Worlds.

Welcome to the public publishing library for [FanVault.Live](https://fanvault.live).

FanVault is exploring a simple idea: **what does it mean to collect fan cards today?*
A card can carry a story, a song, an image, a memory, or a connection to its creator. A collection can become something worth keeping, exploring, sharing, and building upon.  This GitHub library is where we experiment with taking those ideas onto the open web.  How could an artist today use simple and mostly free sofware tools like wordpress and gitbub to build bridge to fan collection.  Today approach to super fan is purely transational and like all bloated industries capture the low hanging fruit <the rich> while leaving the rest unsatisfied, if not, down right disguntled.   The opportunity to merge k-pop with pokemon as envisioned for the millions of aspiring indie musicians built in metaphor as found in Dotland.

And as I build these tools you participate and use them yourself to build your own Dotland and invite all your dots and get them together and do dotty stuff!  or call them fans,  suit yourself.

## 🌎 Explore the Library

We are building a world we call Dotland where ever dot is respected. Its part real and part makebelieve and part game.   Take from it what you want and like and leave the rest.  THere is a puzzle to Dotland and the only way to solve it is to explore.

### 🎨 [Dotland](Dotland/)

*A little dot. A whole world of music.*

Meet Mr. Dot, Pixel, and a growing cast of characters in an imaginary world of music, art, stories, and playful discovery. Dotland is our creative playground for exploring how cards, characters, stories, and collections can connect.  Your welcome to come along and add your stories and ask your friends to come join too.   It's all about Fandom and all that that means but don't ask me or Captain Dot 🎶 as music is our thing and that is what we love!

### 🃏 Cards and Templates

We are developing reusable Markdown templates for creating, documenting, and publishing FanVault cards and drops.  

A starting point for creating cards that walks you through step by step what you need to create your first deck of card is the planning document.  Take a look at it complete it and use it and follow it when you create your first deck and cards

- [Drop Planning Template](Drop-Planning-Template.md)
- **Showcase Template** — Coming soon!
- 
  These templates are designed to be understandable and useful without requiring programming experience.

### 🖼️ Showcases

A showcase brings a collection of cards together into a richer presentation.  Showcase is just the same capability without the game aspects. For example you want to drop and link to 15 second sound bite of something you are working on with poptext maybe about how they can signup for next release you can do it with FanVault showcase.

Our experiments explore how the same content can appear as:

- Markdown documents on GitHub
- Illustrated HTML pages on GitHub Pages
- Stories and articles published through WordPress or Wordland
- Collectible experiences inside FanVault.Live

**One collection. Many ways to experience it.**

## 🌐 Why GitHub?

Most people think of GitHub as a place for programmers.

We're using it as something else: **a public library for creative work.**

Markdown files are easy to write, read, edit, copy, and share. They can contain text, images, links, and structured information.

GitHub provides a public address, file history, and a way to organize collections without building a custom website.

You don't need to be a developer to browse this library.

And that's part of the experiment.


## ✨ Creative Space on the Open Web

Our longer-term vision for FanVault collections that can organize creative content and help make it available beyond the original platform.

Imagine an artist creating a collection of cards, then publishing that collection as a readable document, an illustrated showcase, or a story on their own website.

The goal is not to lock creative work inside one application.

**The goal is to give creators and collectors more ways to keep, share, and experience what they value.**

This repository is an early publishing experiment toward that vision, not a claim that automated Smart Deck publishing is already available.

## 😎 Come Join us!

Participate, create a deck and add some cards and then join your drop and then drop it and see how the whole process works yourself by just signing up (it's free).  With FanVault you can be  both a fan and a creator.  Then get yourself a github installation like this and start wrriting and upload the image and sound files you want to use.  Then when ready you can use the templates provded here to compose and create your drop.  

**The goal is to provide many ways to mix the same data and produce a new view

and that is just the first dot.

## 🔗 Visit FanVault

**[FanVault.Live](https://fanvault.live)** — Collect cards, discover drops, and participate.

**[FanVault on GitHub](https://github.com/FanVaultLive)** — Explore our public repositories.

**[FanVault Open Web Showcase](https://fanvaultlive.github.io)** — Our evolving web publishing experiments.

---

*Made for curious people, creative communities, and the open web.*

**FanVault.Live — Make Your Drop Real.**# [fanvaultlive.github.io] (https://fanvaultlive.github.io/)
FanVault Open Web Publishing


---

## Architecture note — BonBon, RSS.chat, FeedLand, and DirTree (November 24, 2026)

**Status:** Architectural direction and experiment record, not an implementation
authorization or a claim that DirTree imports remote sources today.

### Historical perspective: why BonBon matters

In **“BonBon: A Historical Perspective”**, a text Dave Winer shared on
November 24, 2026, BonBon is described as an exploration of a different
branch of the original Web: ordinary linked documents still use HTTP, URLs,
and hyperlinks, but Markdown becomes a simple common document format.
Markdown did not exist when Tim Berners-Lee proposed the Web in 1989.
The idea is **not** to replace HTML or create a new Internet.

- A short note, a long article, an artist's story, and a card description
  need not be different publishing *species*. Each can begin with an
  independent document and URL.
- An author supplies content; reader software may determine presentation.
  BonBon is a reader, not the owner of a Markdown document.
- Editors, publishers, feed readers, social discussion systems, and
  directories can remain independent and interoperable.
- A public original remains the canonical source; applications point to it
  instead of requiring everyone to move into one platform.

This section summarizes the shared historical framing; it is not a
reproduction of Dave's full essay.

### Parallel tracks, not a mandatory single platform

**Track A — Dotland Express:** The existing curated RSS publication on
GitHub Pages announces approved Markdown Lab documents and independently
authored items. Its RSS subscribers follow the publication.

**Track B — RSS.chat / WordLand:** A creator writes and publishes a post,
and readers can follow the creator's own RSS feed. An experimental example
is Brian's RSS.chat demo feed:
https://demo.rss.chat/users/Brian/rss.xml
This demo is a testing home, **not guaranteed permanent storage**.

**Track C — FeedLand:** A curator follows and organizes other people's
feeds, and may also publish their own posts or linkblog into a personal
RSS feed. A **FeedLand subscription list or category** can be expressed
as **OPML**. The distinction matters:

- **RSS feed:** A stream of *items or posts* that readers subscribe to.
- **OPML outline:** A *list of feeds or sources* assembled by a curator.
- **Markdown URL:** The original document itself, which a compatible
  reader such as BonBon may display.
- **Directory entry:** A pointer with attribution and metadata, not
  necessarily a copy of the original content.

Sources: [FeedLand feed-list documentation](https://docs.feedland.com/yourfeedlist.md),
[FeedLand's own RSS feed](https://docs.feedland.com/yourfeed.md),
and [category OPML exports](https://docs.feedland.com/categories.md).

### DirTree proposal: accept both a creator feed and a curator's list

A person should be able to submit two independent public URLs to DirTree:

1. **“Follow Brian”** — the RSS URL for posts Brian published through
   RSS.chat or any compatible publisher.
2. **“Follow Brian's Picks”** — an OPML URL for Brian's curated FeedLand
   subscriptions, or a FeedLand RSS URL if the intent is to share his
   *own curated posts/linkblog items*.

DirTree should distinguish **author identity, publishing stream, and
curation**. One person may have multiple feeds and multiple curated
outlines; a curated outline is not the same as the posts it points to.
The directory could offer links to the sources and, later, discover
items without demanding a new upload or a DirTree account.

A minimal future ingestion contract would record the submitted URL,
source type (RSS, OPML, Markdown, or other supported web document),
declared title and attribution, original/canonical URL, retrieval and
last-reviewed times, and verification status. The origin stays
authoritative. Curator review should be used before listing untrusted
new sources. Do not silently republish full content or claim verified
authorship from a self-reported feed title.

### Implementation boundary — KISS

- **Already demonstrated:** public Markdown URLs; RSS announcements;
  Dotland Express curation; RSS.chat posts with personal RSS; FeedLand
  RSS subscriptions and OPML lists.
- **Not yet built:** DirTree submission and remote ingestion of arbitrary
  RSS/OPML URLs, automatic federation, or synchronization between
  RSS.chat and Dotland Express.
- **Not the goal:** create another social network, editor, feed reader,
  content silo, or route into FanVault's production Game/COMS database.
- **Future gate:** read-only discovery first; exact URL preservation,
  attribution, anti-spam review, safe parsing, and explicit permission
  before any production integration.

**Principle:** *One original document; many ways to publish, follow,
discuss, curate, and discover it.* Small pieces, loosely joined.
