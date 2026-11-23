# Dotland Open Web Express — Markdown Lab bridge (MD-PUB-003)

**Goal:** Have exactly one subscriber-facing RSS address:
https://fanvaultlive.github.io/dotland/experiment-001/feed.xml

That feed keeps its original Dotland announcements and adds **only articles
approved by a human** in the separate Markdown Lab review queue.

## How it works

1. Anyone uploads a .md file at the isolated Markdown Publisher Preview and
   optionally submits it to RSS review.
2. Lab operator approves the submission in Markdown Lab. **No automatic
   approval**; this mechanism never reads the pending queue.
3. Public \`/feed.xml\` of the Markdown Lab lists approved, still-readable
   documents only.
4. Scheduled GitHub Action (hourly, :17 UTC) or operator's manual run fetches
   that feed, validates expected origin/reader URLs/GUIDs, and replaces only a
   clearly delimited imported block in the *existing* RSS feed.
5. The Action commits only if the RSS file actually changed. FeedLand then
   discovers the update when it next polls its existing subscription.

The first approved item, “one little dot,” is staged inside the proposed
original feed so the first merge would be visible without waiting for cron.

**Important:** The source RSS address points to an *experimental Vercel Preview
deployment*. Its URLs are not guaranteed permanent. A stable public address
must be established before inviting creators or relying on subscriptions for
long-term distribution. The current source address is intentionally pinned
in the bridge script and should not be changed without review.

## Isolation and safety

- Changes limited to this GitHub Pages repository; **no** FanVault Production,
  Supa2, Dropline repositories, Supabase outside Markdown Lab, or existing
  infrastructure deployments are touched.
- Operator-approved items only. Unapproved submissions never appear.
- Importer limits source feed to 256 KB, 100 items, well-formed XML, pinned
  self-link, validated GUIDs, reader URLs, and valid RFC822 dates. It generates
  escaped XML text rather than copying arbitrary markup.
- Existing, manually authored RSS items stay in the file and are not overwritten.
- When a previously approved Markdown item is taken down or no longer listed,
  its managed RSS item is removed on refresh.
- If source fetch/validation fails, the Action stops and does **not** publish
  an empty feed. GitHub Pages keeps serving the prior version.
- Action permissions: repository-only \`contents: write\`; workflow does not
  run shell commands from anonymous content and does not use external tokens.
- Workflow requires deliberate merge into GitHub Pages \`main\`. Until then,
  public feed and current FeedLand subscribers are unaffected.
- The remote source is **not** a perpetual backup. The GitHub-hosted approved
  article and lab-hosted document may have different lifetimes.
- No OPML/DirTree expansion or external URL submissions in this experiment.

## Review/test before merging

Run offline checks in a checkout:
\`\`\`bash
python3 -m unittest discover -s tests -p 'test_refresh_express_feed.py' -v
\`\`\`

After explicit GO for GitHub Pages main:
1. Verify original RSS contains Bowwow, First Automated Dot, and One Little Dot.
2. FeedLand: open **existing** Dotland Open Web Express subscription and refresh
   to see One Little Dot; no second subscription required.
3. GitHub → Actions → *Refresh Dotland Open Web Express* → *Run workflow*.
   It should be idempotent if no new approvals.
4. Publish and approve another disposable test document. Run workflow again
   to confirm automatic import into the original feed.
5. If branch protection or Actions permissions prevent \`git push\`, stop and
   review repository policy; do not create a personal token workaround.

## Scope reminder

The Express curates announcements, not the authors' content or identities.
It is not a blogging platform. Future DirTree indexing should accept valid
publications from external sites without forcing use of Markdown Lab.
