"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const core_1 = require("@fleet-sdk/core");
const yargs_1 = __importDefault(require("yargs"));
const helpers_1 = require("yargs/helpers");
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
async function main() {
    const argv = await (0, yargs_1.default)((0, helpers_1.hideBin)(process.argv)).argv;
    const wallet = argv.wallet;
    // declare var ergo: any;
    if (!wallet) {
        console.error('Error: Wallet address is required.');
        process.exit(1);
    }
    async function getTokensFromFile(wallet) {
        const tokenFile = path.join(__dirname, `../tokens_${wallet}.json`);
        if (!fs.existsSync(tokenFile)) {
            throw new Error('Token file not found');
        }
        const tokensData = JSON.parse(fs.readFileSync(tokenFile, 'utf-8'));
        return tokensData.tokens.map((token) => ({
            tokenId: token.tokenId,
            amount: token.amount // Convert to BigInt
        }));
    }
    async function buildTransaction(wallet) {
        const tokens = await getTokensFromFile(wallet);
        const height = await ergo.get_current_height();
        // Define other transaction parameters
        const inputs = await ergo.get_utxos(); // Add actual inputs as needed
        const unsignedTransaction = new core_1.TransactionBuilder(height)
            .from(inputs)
            .to(new core_1.OutputBuilder('1000000n', wallet).addTokens(tokens))
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
