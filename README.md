
## stacked diffs/cascading rebasing
a tool for myself. tldr if you have a stack of branches/changes: a, b, c, d, .... a change on b would require rebasing c onto b, d onto c, etc. this script just automates that and provides a stack description for every pr in the stack (look at the frontend, api, and backend prs)

note: [git rerere](https://git-scm.com/docs/git-rerere) to record conflicted merge results (to prevent resolving the same conflict up a stack of prs)

these should've been a collection of bash scripts (i dont know bash)
