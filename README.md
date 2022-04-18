# SecureGitlab

Secure GitLab instance using its REST API

## Usage

- generate private token with `api` permissions
- call tool with:

```bash
```bash
./secure_gitlab.py --url http://localhost --private-token 7Ha5jBvMP5G3fsa_ZSLD \
    --disable-public-signup \
    --depromote-users \
    --except-user root
```