# Set up writing-style on claude.ai

Do this once, from any computer. The skill attaches to your Claude account, not to the machine, so after this it works in every browser where you're logged in.

## 1. Get the zip

Download `writing-style-v2.0.0.zip` from the releases page:

https://github.com/realmwell/writing-style/releases/latest

Save it anywhere. It's a small file. Don't unzip it.

## 2. Upload it to claude.ai

1. Go to https://claude.ai and log in.
2. Click your initials in the bottom-left corner, then Settings.
3. Open the Capabilities section. Skills are listed there. If you don't see it, try Settings and then Skills; the tab name has moved before.
4. Find the existing skill named writing-style. That's the old version from February. Remove it, or if there's a replace option, use that.
5. Click Upload skill (or Add skill) and choose the zip you downloaded.
6. Make sure the toggle next to writing-style is on.

You're done with the hard part. The desktop app picks the change up on its own the next time it syncs.

## 3. Tell Claude to use it every time

Skills switch on when Claude decides the task matches. To make that as close to automatic as it gets, give Claude a standing instruction:

1. Settings, then Profile.
2. In the box that asks how Claude should respond to you (personal preferences), paste this:

```
For any writing you produce for me (emails, outreach, posts, copy, speeches, notes, rewrites), always use my writing-style skill and give me only the clean result. For research or analysis, apply only its anti-AI rules. End every writing reply with one line: writing-style: on
```

3. Save.

That last line is your check. If a reply doesn't end with "writing-style: on", the skill didn't run. Say "use writing-style" and it will.

## 4. For the Databricks emails, make a Project

Projects carry their own instructions into every chat inside them, so this is the strongest guarantee available.

1. In the left sidebar, click Projects, then New project. Call it Outreach.
2. Open the project's instructions and paste the same text from step 3.
3. Under project knowledge, add these five files from the repo (download them from GitHub, they're in the `references` folder): `voice-profile.md`, `registers.md`, `anti-ai-patterns.md`, `clarity-rules.md`, `cold-email.md`.
4. Write all outreach inside that project.

## 5. Test it

Start a new chat and type: "Write a reply to my building manager. They want to wait until September to fix the fireplace. I want it done this month."

You should get something that opens "Hi Name," thanks them, gives two or three plain reasons, asks one question, and closes "Thanks so much," then "Max," with "writing-style: on" at the end. If the voice is off, paste the reply back and say "this doesn't sound like me."

## If something looks wrong

The skill's rules live in `SKILL.md` and the `references` folder of this repo. Change a rule there, rebuild the zip (zip up `SKILL.md`, `references`, `scripts`, and `evals`, leaving out `evals/blind_test/private`), and upload again. Version numbers are in `CHANGELOG.md`.
