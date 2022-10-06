# Scenario's to show strenghts and weaknesses of schemathesis
* Show false positives when missing examples
* show workings of additionalProperties / show false positives when not adding additionalProperties: false
* Show workings of required
* Show what happens when missing statuscode from specification
* Show when name is naam with additionalProperties - bi-directional issue
* Show when name is naam without additionalProperties - bi-directional issue
* ...

For example:
change response schema from only returning ID to returning Workshopfollower object

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
.venv/bin/schemathesis run static/openapi.yaml -c all --base-url http://localhost:5000 --show-errors-tracebacks --store-network-log=cassette.yaml
```
