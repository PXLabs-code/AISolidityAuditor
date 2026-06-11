# Glamsterdam Solidity Readiness Report

- **Project**: solmate
- **Readiness findings**: 106

> This report contains Glamsterdam readiness heuristics only. Slither findings are published separately in `audit-report.md` and `findings.json`.

> This report is an early readiness triage for proposed Glamsterdam-related changes. It is not a protocol compatibility guarantee and requires manual review.

## Focus Areas

- Gas repricing and gas-sensitive source patterns
- EVM opcode or low-level call assumptions
- Native ETH transfer logging assumptions
- Block context assumptions around ePBS and Block-Level Access Lists
- Contract-size watch points

## Findings

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/DSTestPlus.t.sol:60`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
58:         bytes32 freeMem2;
59: 
60:         assembly {
61:             scratchSpace1 := mload(0)
62:             scratchSpace2 := mload(32)
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `test/ERC1155.t.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Manual review required**: Yes

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:880`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
878:         uint256[] memory normalizedAmounts = new uint256[](minLength);
879: 
880:         for (uint256 i = 0; i < minLength; i++) {
881:             uint256 id = ids[i];
882: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:895`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
893:         token.batchMint(to, normalizedIds, normalizedAmounts, mintData);
894: 
895:         for (uint256 i = 0; i < normalizedIds.length; i++) {
896:             uint256 id = normalizedIds[i];
897: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:914`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
912:         uint256[] memory normalizedAmounts = new uint256[](minLength);
913: 
914:         for (uint256 i = 0; i < minLength; i++) {
915:             uint256 id = ids[i];
916: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:935`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
933:         assertBytesEq(to.batchData(), mintData);
934: 
935:         for (uint256 i = 0; i < normalizedIds.length; i++) {
936:             uint256 id = normalizedIds[i];
937: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:979`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
977:         uint256[] memory normalizedBurnAmounts = new uint256[](minLength);
978: 
979:         for (uint256 i = 0; i < minLength; i++) {
980:             uint256 id = ids[i];
981: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:996`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
994:         token.batchBurn(to, normalizedIds, normalizedBurnAmounts);
995: 
996:         for (uint256 i = 0; i < normalizedIds.length; i++) {
997:             uint256 id = normalizedIds[i];
998: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1111`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1109:         uint256[] memory normalizedTransferAmounts = new uint256[](minLength);
1110: 
1111:         for (uint256 i = 0; i < minLength; i++) {
1112:             uint256 id = ids[i];
1113: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1134`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1132:         token.safeBatchTransferFrom(from, to, normalizedIds, normalizedTransferAmounts, transferData);
1133: 
1134:         for (uint256 i = 0; i < normalizedIds.length; i++) {
1135:             uint256 id = normalizedIds[i];
1136: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1159`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1157:         uint256[] memory normalizedTransferAmounts = new uint256[](minLength);
1158: 
1159:         for (uint256 i = 0; i < minLength; i++) {
1160:             uint256 id = ids[i];
1161: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1188`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1186:         assertBytesEq(to.batchData(), transferData);
1187: 
1188:         for (uint256 i = 0; i < normalizedIds.length; i++) {
1189:             uint256 id = normalizedIds[i];
1190:             uint256 transferAmount = userTransferOrBurnAmounts[from][id];
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1208`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1206:         uint256[] memory normalizedIds = new uint256[](minLength);
1207: 
1208:         for (uint256 i = 0; i < minLength; i++) {
1209:             uint256 id = ids[i];
1210:             address to = tos[i] == address(0) || tos[i].code.length > 0 ? address(0xBEEF) : tos[i];
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1226`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1224:         uint256[] memory balances = token.balanceOfBatch(normalizedTos, normalizedIds);
1225: 
1226:         for (uint256 i = 0; i < normalizedTos.length; i++) {
1227:             assertEq(balances[i], token.balanceOf(normalizedTos[i], normalizedIds[i]));
1228:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1392`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1390:         uint256[] memory normalizedTransferAmounts = new uint256[](minLength);
1391: 
1392:         for (uint256 i = 0; i < minLength; i++) {
1393:             uint256 id = ids[i];
1394: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1430`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1428:         uint256[] memory normalizedTransferAmounts = new uint256[](minLength);
1429: 
1430:         for (uint256 i = 0; i < minLength; i++) {
1431:             uint256 id = ids[i];
1432: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1468`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1466:         uint256[] memory normalizedTransferAmounts = new uint256[](minLength);
1467: 
1468:         for (uint256 i = 0; i < minLength; i++) {
1469:             uint256 id = ids[i];
1470: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1512`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1510:         uint256[] memory normalizedTransferAmounts = new uint256[](minLength);
1511: 
1512:         for (uint256 i = 0; i < minLength; i++) {
1513:             uint256 id = ids[i];
1514: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1556`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1554:         uint256[] memory normalizedTransferAmounts = new uint256[](minLength);
1555: 
1556:         for (uint256 i = 0; i < minLength; i++) {
1557:             uint256 id = ids[i];
1558: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1615`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1613:         uint256[] memory normalizedAmounts = new uint256[](minLength);
1614: 
1615:         for (uint256 i = 0; i < minLength; i++) {
1616:             uint256 id = ids[i];
1617: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1643`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1641:         uint256[] memory normalizedAmounts = new uint256[](minLength);
1642: 
1643:         for (uint256 i = 0; i < minLength; i++) {
1644:             uint256 id = ids[i];
1645: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1671`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1669:         uint256[] memory normalizedAmounts = new uint256[](minLength);
1670: 
1671:         for (uint256 i = 0; i < minLength; i++) {
1672:             uint256 id = ids[i];
1673: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1699`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1697:         uint256[] memory normalizedAmounts = new uint256[](minLength);
1698: 
1699:         for (uint256 i = 0; i < minLength; i++) {
1700:             uint256 id = ids[i];
1701: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/ERC1155.t.sol:1741`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
1739:         uint256[] memory normalizedBurnAmounts = new uint256[](minLength);
1740: 
1741:         for (uint256 i = 0; i < minLength; i++) {
1742:             uint256 id = ids[i];
1743: 
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `test/ERC20.t.sol:49`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Manual review required**: Yes

```solidity
47:         token.mint(address(this), 1e18);
48: 
49:         assertTrue(token.transfer(address(0xBEEF), 1e18));
50:         assertEq(token.totalSupply(), 1e18);
51: 
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:100`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
98:                     "\x19\x01",
99:                     token.DOMAIN_SEPARATOR(),
100:                     keccak256(abi.encode(PERMIT_TYPEHASH, owner, address(0xCAFE), 1e18, 0, block.timestamp))
101:                 )
102:             )
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:105`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
103:         );
104: 
105:         token.permit(owner, address(0xCAFE), 1e18, block.timestamp, v, r, s);
106: 
107:         assertEq(token.allowance(owner, address(0xCAFE)), 1e18);
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `test/ERC20.t.sol:113`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Manual review required**: Yes

```solidity
111:     function testFailTransferInsufficientBalance() public {
112:         token.mint(address(this), 0.9e18);
113:         token.transfer(address(0xBEEF), 1e18);
114:     }
115: 
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:148`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
146:                     "\x19\x01",
147:                     token.DOMAIN_SEPARATOR(),
148:                     keccak256(abi.encode(PERMIT_TYPEHASH, owner, address(0xCAFE), 1e18, 1, block.timestamp))
149:                 )
150:             )
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:153`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
151:         );
152: 
153:         token.permit(owner, address(0xCAFE), 1e18, block.timestamp, v, r, s);
154:     }
155: 
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:166`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
164:                     "\x19\x01",
165:                     token.DOMAIN_SEPARATOR(),
166:                     keccak256(abi.encode(PERMIT_TYPEHASH, owner, address(0xCAFE), 1e18, 0, block.timestamp))
167:                 )
168:             )
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:171`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
169:         );
170: 
171:         token.permit(owner, address(0xCAFE), 1e18, block.timestamp + 1, v, r, s);
172:     }
173: 
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:175`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
173: 
174:     function testFailPermitPastDeadline() public {
175:         uint256 oldTimestamp = block.timestamp;
176:         uint256 privateKey = 0xBEEF;
177:         address owner = hevm.addr(privateKey);
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:190`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
188:         );
189: 
190:         hevm.warp(block.timestamp + 1);
191:         token.permit(owner, address(0xCAFE), 1e18, oldTimestamp, v, r, s);
192:     }
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:204`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
202:                     "\x19\x01",
203:                     token.DOMAIN_SEPARATOR(),
204:                     keccak256(abi.encode(PERMIT_TYPEHASH, owner, address(0xCAFE), 1e18, 0, block.timestamp))
205:                 )
206:             )
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:209`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
207:         );
208: 
209:         token.permit(owner, address(0xCAFE), 1e18, block.timestamp, v, r, s);
210:         token.permit(owner, address(0xCAFE), 1e18, block.timestamp, v, r, s);
211:     }
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:210`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
208: 
209:         token.permit(owner, address(0xCAFE), 1e18, block.timestamp, v, r, s);
210:         token.permit(owner, address(0xCAFE), 1e18, block.timestamp, v, r, s);
211:     }
212: 
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `test/ERC20.t.sol:254`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Manual review required**: Yes

```solidity
252:         token.mint(address(this), amount);
253: 
254:         assertTrue(token.transfer(from, amount));
255:         assertEq(token.totalSupply(), amount);
256: 
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:300`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
298:     ) public {
299:         uint256 privateKey = privKey;
300:         if (deadline < block.timestamp) deadline = block.timestamp;
301:         if (privateKey == 0) privateKey = 1;
302: 
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `test/ERC20.t.sol:341`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Manual review required**: Yes

```solidity
339: 
340:         token.mint(address(this), mintAmount);
341:         token.transfer(to, sendAmount);
342:     }
343: 
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:385`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
383:         uint256 nonce
384:     ) public {
385:         if (deadline < block.timestamp) deadline = block.timestamp;
386:         if (privateKey == 0) privateKey = 1;
387:         if (nonce == 0) nonce = 1;
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:411`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
409:         uint256 deadline
410:     ) public {
411:         if (deadline < block.timestamp) deadline = block.timestamp;
412:         if (privateKey == 0) privateKey = 1;
413: 
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:436`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
434:         uint256 deadline
435:     ) public {
436:         deadline = bound(deadline, 0, block.timestamp - 1);
437:         if (privateKey == 0) privateKey = 1;
438: 
```

### [Informational] glamsterdam-block-context

- **Location**: `test/ERC20.t.sol:461`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
459:         uint256 deadline
460:     ) public {
461:         if (deadline < block.timestamp) deadline = block.timestamp;
462:         if (privateKey == 0) privateKey = 1;
463: 
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `test/ERC20.t.sol:529`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Manual review required**: Yes

```solidity
527: 
528:     function transfer(address to, uint256 amount) public {
529:         token.transfer(to, amount);
530:     }
531: }
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `test/ERC6909.t.sol:50`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Manual review required**: Yes

```solidity
48: 
49:         hevm.prank(sender);
50:         token.transfer(address(0xBEEF), 1337, 70);
51: 
52:         assertEq(token.balanceOf(sender, 1337), 30);
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `test/ERC6909.t.sol:212`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Manual review required**: Yes

```solidity
210: 
211:         hevm.prank(sender);
212:         token.transfer(receiver, id, transferAmount);
213: 
214:         if (sender == receiver) {
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `test/ERC6909.t.sol:311`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Manual review required**: Yes

```solidity
309: 
310:         hevm.prank(sender);
311:         token.transfer(receiver, id, amount);
312:     }
313: 
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `test/ERC6909.t.sol:326`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Manual review required**: Yes

```solidity
324: 
325:         hevm.prank(sender);
326:         token.transfer(receiver, id, amount);
327: 
328:         token.mint(sender, id, overflowAmount);
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `test/ERC6909.t.sol:331`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Manual review required**: Yes

```solidity
329: 
330:         hevm.prank(sender);
331:         token.transfer(receiver, id, overflowAmount);
332:     }
333: 
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `test/ERC721.t.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Manual review required**: Yes

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/FixedPointMathLib.t.sol:291`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
289:         unchecked {
290:             x >>= 128;
291:             while (x != 0) {
292:                 assertEq(FixedPointMathLib.sqrt(x * x), x);
293:                 x >>= 1;
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/FixedPointMathLib.t.sol:306`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
304:             z = y;
305:             uint256 x = y / 2 + 1;
306:             while (x < z) {
307:                 z = x;
308:                 x = (y / x + x) / 2;
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/LibString.t.sol:66`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
64:         bytes32 expected;
65: 
66:         assembly {
67:             // Imagine a high level allocation writing something to the current free memory.
68:             // Should have sufficient higher order bits for this to be visible
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/LibString.t.sol:86`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
84:         uint256 freememptr;
85:         // Make the next 4 bytes of the free memory dirty
86:         assembly {
87:             let dirty := not(0)
88:             freememptr := mload(0x40)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/LibString.t.sol:99`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
97:         bytes32 data;
98:         bytes32 expected;
99:         assembly {
100:             freememptr := str
101:             len := mload(str)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/LibString.t.sol:111`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
109:         emit log_named_uint("len: ", len);
110:         emit log_named_bytes32("data: ", data);
111:         assembly {
112:             freememptr := mload(0x40)
113:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/LibString.t.sol:130`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
128:     uint256 temp = value;
129:     uint256 digits;
130:     while (temp != 0) {
131:         digits++;
132:         temp /= 10;
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/LibString.t.sol:135`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
133:     }
134:     bytes memory buffer = new bytes(digits);
135:     while (value != 0) {
136:         digits -= 1;
137:         buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `test/SafeTransferLib.t.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Manual review required**: Yes

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `test/SafeTransferLib.t.sol:571`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Manual review required**: Yes

```solidity
569:         // We cast to MissingReturnToken here because it won't check
570:         // that there was return data, which accommodates all tokens.
571:         MissingReturnToken(token).transfer(from, amount);
572: 
573:         uint256 preBal = ERC20(token).balanceOf(to);
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/utils/DSTestPlus.sol:20`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
18:     modifier brutalizeMemory(bytes memory brutalizeWith) {
19:         /// @solidity memory-safe-assembly
20:         assembly {
21:             // Fill the 64 bytes of scratch space with the data.
22:             pop(
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `test/utils/DSTestPlus.sol:143`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
141:         require(a.length == b.length, "LENGTH_MISMATCH");
142: 
143:         for (uint256 i = 0; i < a.length; i++) {
144:             assertEq(a[i], b[i]);
145:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/utils/weird-tokens/ReturnsGarbageToken.sol:59`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
57:         bytes memory _garbage = garbage;
58: 
59:         assembly {
60:             return(add(_garbage, 32), mload(_garbage))
61:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/utils/weird-tokens/ReturnsGarbageToken.sol:77`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
75:         bytes memory _garbage = garbage;
76: 
77:         assembly {
78:             return(add(_garbage, 32), mload(_garbage))
79:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/utils/weird-tokens/ReturnsGarbageToken.sol:103`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
101:         bytes memory _garbage = garbage;
102: 
103:         assembly {
104:             return(add(_garbage, 32), mload(_garbage))
105:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/utils/weird-tokens/ReturnsTooLittleToken.sol:47`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
45: 
46:     function approve(address, uint256) public virtual {
47:         assembly {
48:             mstore(0, 0x0100000000000000000000000000000000000000000000000000000000000000)
49:             return(0, 8)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/utils/weird-tokens/ReturnsTooLittleToken.sol:54`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
52: 
53:     function transfer(address, uint256) public virtual {
54:         assembly {
55:             mstore(0, 0x0100000000000000000000000000000000000000000000000000000000000000)
56:             return(0, 8)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/utils/weird-tokens/ReturnsTooLittleToken.sol:65`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
63:         uint256
64:     ) public virtual {
65:         assembly {
66:             mstore(0, 0x0100000000000000000000000000000000000000000000000000000000000000)
67:             return(0, 8)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/utils/weird-tokens/ReturnsTooMuchToken.sol:51`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
49:         emit Approval(msg.sender, spender, amount);
50: 
51:         assembly {
52:             mstore(0, 1)
53:             return(0, 4096)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/utils/weird-tokens/ReturnsTooMuchToken.sol:68`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
66:         emit Transfer(msg.sender, to, amount);
67: 
68:         assembly {
69:             mstore(0, 1)
70:             return(0, 4096)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `test/utils/weird-tokens/ReturnsTooMuchToken.sol:93`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
91:         emit Transfer(from, to, amount);
92: 
93:         assembly {
94:             mstore(0, 1)
95:             return(0, 4096)
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `tokens/ERC1155.sol:93`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
91:         uint256 amount;
92: 
93:         for (uint256 i = 0; i < ids.length; ) {
94:             id = ids[i];
95:             amount = amounts[i];
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `tokens/ERC1155.sol:131`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
129:         // the array index counter which cannot possibly overflow.
130:         unchecked {
131:             for (uint256 i = 0; i < owners.length; ++i) {
132:                 balances[i] = balanceOf[owners[i]][ids[i]];
133:             }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `tokens/ERC1155.sol:181`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
179:         require(idsLength == amounts.length, "LENGTH_MISMATCH");
180: 
181:         for (uint256 i = 0; i < idsLength; ) {
182:             balanceOf[to][ids[i]] += amounts[i];
183: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `tokens/ERC1155.sol:211`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Manual review required**: Yes

```solidity
209:         require(idsLength == amounts.length, "LENGTH_MISMATCH");
210: 
211:         for (uint256 i = 0; i < idsLength; ) {
212:             balanceOf[from][ids[i]] -= amounts[i];
213: 
```

### [Informational] glamsterdam-block-context

- **Location**: `tokens/ERC20.sol:125`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Manual review required**: Yes

```solidity
123:         bytes32 s
124:     ) public virtual {
125:         require(deadline >= block.timestamp, "PERMIT_DEADLINE_EXPIRED");
126: 
127:         // Unchecked because the only math done is incrementing
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/CREATE3.sol:46`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
44:         address proxy;
45:         /// @solidity memory-safe-assembly
46:         assembly {
47:             // Deploy a new contract with our pre-made bytecode via CREATE2.
48:             // We start 32 bytes into the code to avoid copying the byte length.
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `utils/CREATE3.sol:54`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Manual review required**: Yes

```solidity
52: 
53:         deployed = getDeployed(salt);
54:         (bool success, ) = proxy.call{value: value}(creationCode);
55:         require(success && deployed.code.length != 0, "INITIALIZATION_FAILED");
56:     }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/FixedPointMathLib.sol:42`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
40:     ) internal pure returns (uint256 z) {
41:         /// @solidity memory-safe-assembly
42:         assembly {
43:             // Equivalent to require(denominator != 0 && (y == 0 || x <= type(uint256).max / y))
44:             if iszero(mul(denominator, iszero(mul(y, gt(x, div(MAX_UINT256, y)))))) {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/FixedPointMathLib.sol:59`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
57:     ) internal pure returns (uint256 z) {
58:         /// @solidity memory-safe-assembly
59:         assembly {
60:             // Equivalent to require(denominator != 0 && (y == 0 || x <= type(uint256).max / y))
61:             if iszero(mul(denominator, iszero(mul(y, gt(x, div(MAX_UINT256, y)))))) {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/FixedPointMathLib.sol:77`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
75:     ) internal pure returns (uint256 z) {
76:         /// @solidity memory-safe-assembly
77:         assembly {
78:             switch x
79:             case 0 {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/FixedPointMathLib.sol:166`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
164:     function sqrt(uint256 x) internal pure returns (uint256 z) {
165:         /// @solidity memory-safe-assembly
166:         assembly {
167:             let y := x // We start y at x, which will help us make our initial estimate.
168: 
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/FixedPointMathLib.sol:231`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
229:     function unsafeMod(uint256 x, uint256 y) internal pure returns (uint256 z) {
230:         /// @solidity memory-safe-assembly
231:         assembly {
232:             // Mod x by y. Note this will return
233:             // 0 instead of reverting if y is zero.
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/FixedPointMathLib.sol:240`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
238:     function unsafeDiv(uint256 x, uint256 y) internal pure returns (uint256 r) {
239:         /// @solidity memory-safe-assembly
240:         assembly {
241:             // Divide x by y. Note this will return
242:             // 0 instead of reverting if y is zero.
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/FixedPointMathLib.sol:249`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
247:     function unsafeDivUp(uint256 x, uint256 y) internal pure returns (uint256 z) {
248:         /// @solidity memory-safe-assembly
249:         assembly {
250:             // Add 1 to x * y if x % y > 0. Note this will
251:             // return 0 instead of reverting if y is zero.
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/LibString.sol:15`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
13: 
14:             /// @solidity memory-safe-assembly
15:             assembly {
16:                 // Note: This is only safe because we over-allocate memory
17:                 // and write the string from right to left in toString(uint256),
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/LibString.sol:31`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
29:     function toString(uint256 value) internal pure returns (string memory str) {
30:         /// @solidity memory-safe-assembly
31:         assembly {
32:             // The maximum value of a uint256 contains 78 digits (1 byte per digit), but we allocate 160 bytes
33:             // to keep the free memory pointer word aligned. We'll need 1 word for the length, 1 word for the
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/MerkleProofLib.sol:14`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
12:     ) internal pure returns (bool isValid) {
13:         /// @solidity memory-safe-assembly
14:         assembly {
15:             if proof.length {
16:                 // Left shifting by 5 is like multiplying by 32.
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SSTORE2.sol:38`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
36: 
37:         /// @solidity memory-safe-assembly
38:         assembly {
39:             // Deploy a new contract with the generated creation code.
40:             // We start 32 bytes into the code to avoid copying the byte length.
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SSTORE2.sol:84`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
82:     ) private view returns (bytes memory data) {
83:         /// @solidity memory-safe-assembly
84:         assembly {
85:             // Get a pointer to some free memory.
86:             data := mload(0x40)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SafeTransferLib.sol:18`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
16: 
17:         /// @solidity memory-safe-assembly
18:         assembly {
19:             // Transfer the ETH and store if it succeeded or not.
20:             success := call(gas(), to, amount, 0, 0, 0, 0)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SafeTransferLib.sol:39`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
37: 
38:         /// @solidity memory-safe-assembly
39:         assembly {
40:             // Get a pointer to some free memory.
41:             let freeMemoryPointer := mload(0x40)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SafeTransferLib.sol:71`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
69: 
70:         /// @solidity memory-safe-assembly
71:         assembly {
72:             // Get a pointer to some free memory.
73:             let freeMemoryPointer := mload(0x40)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SafeTransferLib.sol:102`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
100: 
101:         /// @solidity memory-safe-assembly
102:         assembly {
103:             // Get a pointer to some free memory.
104:             let freeMemoryPointer := mload(0x40)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SignedWadMath.sol:11`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
9: function toWadUnsafe(uint256 x) pure returns (int256 r) {
10:     /// @solidity memory-safe-assembly
11:     assembly {
12:         // Multiply x by 1e18.
13:         r := mul(x, 1000000000000000000)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SignedWadMath.sol:22`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
20: function toDaysWadUnsafe(uint256 x) pure returns (int256 r) {
21:     /// @solidity memory-safe-assembly
22:     assembly {
23:         // Multiply x by 1e18 and then divide it by 86400.
24:         r := div(mul(x, 1000000000000000000), 86400)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SignedWadMath.sol:33`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
31: function fromDaysWadUnsafe(int256 x) pure returns (uint256 r) {
32:     /// @solidity memory-safe-assembly
33:     assembly {
34:         // Multiply x by 86400 and then divide it by 1e18.
35:         r := div(mul(x, 86400), 1000000000000000000)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SignedWadMath.sol:42`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
40: function unsafeWadMul(int256 x, int256 y) pure returns (int256 r) {
41:     /// @solidity memory-safe-assembly
42:     assembly {
43:         // Multiply x by y and divide by 1e18.
44:         r := sdiv(mul(x, y), 1000000000000000000)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SignedWadMath.sol:52`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
50: function unsafeWadDiv(int256 x, int256 y) pure returns (int256 r) {
51:     /// @solidity memory-safe-assembly
52:     assembly {
53:         // Multiply x by 1e18 and divide it by y.
54:         r := sdiv(mul(x, 1000000000000000000), y)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SignedWadMath.sol:60`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
58: function wadMul(int256 x, int256 y) pure returns (int256 r) {
59:     /// @solidity memory-safe-assembly
60:     assembly {
61:         // Store x * y in r for now.
62:         r := mul(x, y)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SignedWadMath.sol:86`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
84: function wadDiv(int256 x, int256 y) pure returns (int256 r) {
85:     /// @solidity memory-safe-assembly
86:     assembly {
87:         // Store x * 1e18 in r for now.
88:         r := mul(x, 1000000000000000000)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SignedWadMath.sol:146`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
144: 
145:         /// @solidity memory-safe-assembly
146:         assembly {
147:             // Div in assembly because solidity adds a zero check despite the unchecked.
148:             // The q polynomial won't have zeros in the domain as all its roots are complex.
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SignedWadMath.sol:175`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
173: 
174:         /// @solidity memory-safe-assembly
175:         assembly {
176:             r := shl(7, lt(0xffffffffffffffffffffffffffffffff, x))
177:             r := or(r, shl(6, lt(0xffffffffffffffff, shr(r, x))))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SignedWadMath.sol:212`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
210:         q = ((q * x) >> 96) + 909429971244387300277376558375;
211:         /// @solidity memory-safe-assembly
212:         assembly {
213:             // Div in assembly because solidity adds a zero check despite the unchecked.
214:             // The q polynomial is known not to have zeros in the domain.
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SignedWadMath.sol:241`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Manual review required**: Yes

```solidity
239: function unsafeDiv(int256 x, int256 y) pure returns (int256 r) {
240:     /// @solidity memory-safe-assembly
241:     assembly {
242:         // Divide x by y.
243:         r := sdiv(x, y)
```

## Limitations

- Glamsterdam EIPs are still under consideration and may change.
- Readiness heuristics are separate from Slither static-analysis evidence.
- Findings are review prompts, not vulnerability claims.