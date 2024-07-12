import { OutputBuilder, TransactionBuilder } from "@fleet-sdk/core";
import axios from 'axios';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import * as fs from 'fs';
import * as path from 'path';

declare var ergo: any;

async function main() {
    const argv = await yargs(hideBin(process.argv)).argv;
    const wallet = argv.wallet as string;
    // declare var ergo: any;


    if (!wallet) {
        console.error('Error: Wallet address is required.');
        process.exit(1);
    }

    async function getTokensFromFile(wallet: string) {
        const tokenFile = path.join(__dirname, `../tokens_${wallet}.json`);
        if (!fs.existsSync(tokenFile)) {
            throw new Error('Token file not found');
        }

        const tokensData = JSON.parse(fs.readFileSync(tokenFile, 'utf-8'));
        return tokensData.tokens.map((token: { tokenId: string, amount: string }) => ({
            tokenId: token.tokenId,
            amount: token.amount // Convert to BigInt
        }));
    }

    async function buildTransaction(wallet: string) {
        const tokens = await getTokensFromFile(wallet);
        const height = await ergo.get_current_height();

        // Define other transaction parameters
        const inputs = await ergo.get_utxos();  // Add actual inputs as needed

        const unsignedTransaction = new TransactionBuilder(height)
            .from(inputs)
            .to(
                new OutputBuilder('1000000n', wallet).addTokens(tokens)
            )
            .sendChangeTo(await ergo.get_change_address())
            .payMinFee()
            .build();

        console.log(unsignedTransaction);
    }

    // Start building the transaction with the wallet from command line arguments
    buildTransaction(wallet).catch(error => {
        console.error(error);
        process.exit(1);
    });
}

main().catch(error => {
    console.error(error);
    process.exit(1);
});
