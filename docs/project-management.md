# Project Management

## Contributing Idea's

If you'd like to make an enhancement request you can do so via [GitHub issues](https://github.com/intel-ctrlsys/actsys/issues). In general the more information provided in the request, the more likely it will be accepted and worked on by community members. A few good items to include in your enhancement request are:
- A concise description and valid use case.
- Impact to users.
- Impact to APIs. (Is this a backward compatible enhancement?)
- Estimated effort or affected portions of the project.

This enhancement request will them be tagged _enhancement-review_ and reviewed in the next [community meeting](#community-meetings).

## Bug reports

Bug reports should be reported via [GitHub issues](https://github.com/intel-ctrlsys/actsys/issues). In your report, please clearly outline the following:
- A description
- Execution environment (if applicable).
- Steps to reproduce
- Impact to users
- Workaround (If known)

A member of the actsys-contributor team will triage reports as they are received. This triage should include:
- Confirmation that it is reproducible
- A suggested priority for a fix. This can be _PHigh PMed PLow_ or _wont_fix_.

## Code contributions

To contribute to actsys, [create a pull request](https://help.github.com/articles/creating-a-pull-request/). For a pull request to be accepted, it should adhere to the following criteria:
- They are based on an enhancement request or bug report, or are suggesting one of the two. (Note: in the ladder case, a review of your enhancement must still occur via [community meetings][#community-meetings].)
- Code should be complete. Complete means that you've filled all the criteria set in the enhancement request and there is no further work to at this time.
- Code should pass [testing criteria][#testing-criteria]
- Code should pass [static scan analysis criteria][#static-scan-criteria]
- Code should build via the accepted build process
- Code should have at least on review from the [actsys-contributors team][#actsys-integrators]

### Testing Criteria

All submitted code should be tested. Unit test should cover 80% of all statements and 70% of branches.

GitHub will ensure these checks pass, but you can run them locally using:

```
make test
```

> Note: Coverage numbers are determined by GitHub via a travis-ci process. It doesn't matter if the numbers appear differently on another machine, GitHub wins.

### Static scan criteria

All submitted code should be scanned for consistency. A rating of 8+ out of 10 is required to submit code into master. Static scan analysis uses `pylint`, and rules are defined in the `pylintrc` file in the source repo.

GitHub will ensure your code passes this scan, but you can check locally using:

```
make pylint
```

## Teams

Actsys consists of two teams, *actsys-contributors* and *actsys-integrators*. All members of *actsys-integrators* are also members of *actsys-contributors*. In other words, you cannot be an integrator without being a contributor.

### actsys-contributors

Trusted members of actsys. They are responsible for code-reviews, bug triage and keeping themselves up to date with the project.

### actsys-integrators

The primary role of the *actsys-integrators* team is to be gatekeepers into the master branch. They accept or suggest improvements to pull-requests. To accept pull requests all they follow the critera outlined in this document.

These members are expected to attend the regular community meetings. They should know the current architecture and direction of the project.

## Community Meetings

Regular community meetings will be held. The agenda for this meeting is as follows:
- Review reported bugs since last meeting, for each bug:
  - Determine priority
  - Set a [Milestone] for a fix
  - Ask for volunteers to attempt a fix
- Review enhancement requests since last meeting, for each enhancement request:
  - Discuss plausibility of this request, and it if fits into project plans.
  - Accept, reject, or request changes for this request.
  - Set the appropriate tag on the enhancement request (GitHub issue): _enhancement-accepted, enhancement-rejected_ or _enhancement-needs-improvement_.
  - If accepted, set a [Milestone] for completion.
- Opens
- Project Architecture Review, a presentation given by invitation

> TODO: Determine online medium and cadence of this meeting.


[Milestone]: https://help.github.com/articles/about-milestones/
