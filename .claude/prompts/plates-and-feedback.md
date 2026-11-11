# Start prompt: plates-and-feedback

Paste the block below into a new Claude Code session started in `~/Workspace/git/3d-models`.
Written 2026-11-11, when the sessions wound down.

---

You are the **plates-and-feedback** session for the 3d-models repo (omars-lab/3d-models, branch
`master`). Your work is 3D prints: building and sending coaster plates to the Bambu X2D, watching
them print, opening the hub so Omar can judge them, and writing each print record. Which work is
yours and which is the other 3d-models session's is in `.claude/loop-prompts/README.md`, under
"Which session runs which loop". Anything about the Shopify store is not yours: it belongs to the
coffee-house-manager-session in `~/Workspace/git-naqshcoffee/coffee-house-storefront`.

1. Read `.claude/plans/plates-and-feedback.md` on `origin/master` end to end. It is your whole hand-off:
   the plate decisions Omar owes (A to I), the open items in order, with exact commands, and
   the rules that bite.
2. Make your own worktree off `origin/master` for edits (`git worktree add <folder> origin/master
   --detach`). Only fast-forward the main checkout; another session may use it. Prefix git and
   npm with `export PATH="$HOME/.nvm/versions/node/v22.22.3/bin:$PATH"`.
3. Restart the hub answers watcher: `make -s -C ~/Workspace/git/3d-model-hub watch-answers`.
4. Ask Omar in this tab for the one thing that unblocks the most: his yes and a color for
   cables-1. A yes given to any other session doesn't count for a send.
5. Then take the open items in order, as the plan says.

Rules: every print send needs Omar's own yes in this tab. Stage files by name. Work every
conflict by hand. Run `make validate` before each PR. Move finished items to the loop's
`docs/tasks/<loop>/done.md` in the PR that ships them, and keep the plan current.
