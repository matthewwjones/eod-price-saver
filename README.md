# EOD Price Saver

Fetches end-of-day closing prices for a configured list of instruments from the [EODHD](https://eodhd.com) API and emails them via AWS SES. Runs daily as an AWS Lambda function.

## How it works

On each invocation the Lambda reads `instrument-codes.txt`, fetches the closing price for each instrument from the EODHD REST API, and sends an email summarising the results.

## Configuration

### Lambda environment variables

| Variable | Description |
|---|---|
| `EOD_LOADER_API_TOKEN` | EODHD API key |
| `EOD_LOADER_AWS_REGION` | AWS region for SES (e.g. `eu-west-1`) |
| `EOD_LOADER_EMAIL_TO` | Recipient email address |
| `EOD_LOADER_EMAIL_FROM` | Verified SES sender address |

### Instruments

Add or remove instruments by editing `instrument-codes.txt` — one code per line (e.g. `ISF.LSE`). Lines beginning with `#` are treated as comments and ignored. The file is bundled into the Lambda deployment package on each deploy.

## Running locally

Fetches and logs prices without sending email:

```bash
EOD_LOADER_API_TOKEN=<your-token> python -m src.__main__
```

Reads instrument codes from `instrument-codes.txt` at the repo root.

## Deployment

Pushing to `main` triggers the [deploy workflow](.github/workflows/deploy-lambda.yml), which packages the source and dependencies and deploys to the `eod-price-saver` Lambda function.

The Lambda handler is `src.__main__.lambda_handler`.

## Running tests

```bash
pytest
