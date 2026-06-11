# Glamsterdam Solidity Readiness Report

- **Project**: openzeppelin-contracts
- **Readiness findings**: 609
- **Upgrade references**: EIP-7773 (Glamsterdam meta), forkcast.org

> This report contains Glamsterdam readiness heuristics only. Slither findings are published separately in `audit-report.md` and `findings.json`.

> This report is an early readiness triage for proposed Glamsterdam-related changes. It is not a protocol compatibility guarantee and requires manual review. Rule confidence below reflects how often a keyword match is expected to deserve action: low-confidence rules are intentionally high-recall review prompts.

## Focus Areas

- Gas repricing and gas-sensitive source patterns
- EVM opcode or low-level call assumptions
- Native ETH transfer logging assumptions
- Block context assumptions around ePBS and Block-Level Access Lists
- Contract-size watch points

## Summary by detector

| Detector | Rule confidence | Count |
|----------|-----------------|------:|
| `glamsterdam-block-context` | medium | 34 |
| `glamsterdam-contract-size-watch` | low | 12 |
| `glamsterdam-eth-transfer-assumption` | medium | 10 |
| `glamsterdam-gas-sensitive-loop` | low | 104 |
| `glamsterdam-low-level-evm` | low | 449 |

## Findings

### [Informational] glamsterdam-block-context

- **Location**: `access/extensions/AccessControlDefaultAdminRules.sol:205`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
203:      */
204:     function _beginDefaultAdminTransfer(address newAdmin) internal virtual {
205:         uint48 newSchedule = SafeCast.toUint48(block.timestamp) + defaultAdminDelay();
206:         _setPendingDefaultAdmin(newAdmin, newSchedule);
207:         emit DefaultAdminTransferScheduled(newAdmin, newSchedule);
```

### [Informational] glamsterdam-block-context

- **Location**: `access/extensions/AccessControlDefaultAdminRules.sol:265`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
263:      */
264:     function _changeDefaultAdminDelay(uint48 newDelay) internal virtual {
265:         uint48 newSchedule = SafeCast.toUint48(block.timestamp) + _delayChangeWait(newDelay);
266:         _setPendingDelay(newDelay, newSchedule);
267:         emit DefaultAdminDelayChangeScheduled(newDelay, newSchedule);
```

### [Informational] glamsterdam-block-context

- **Location**: `access/extensions/AccessControlDefaultAdminRules.sol:370`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
368:      */
369:     function _hasSchedulePassed(uint48 schedule) private view returns (bool) {
370:         return schedule < block.timestamp;
371:     }
372: }
```

### [Informational] glamsterdam-block-context

- **Location**: `access/extensions/IAccessControlDefaultAdminRules.sol:153`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
151:      * The schedule is designed for two scenarios:
152:      *
153:      * - When the delay is changed for a larger one the schedule is `block.timestamp + newDelay` capped by
154:      * {defaultAdminDelayIncreaseWait}.
155:      * - When the delay is changed for a shorter one, the schedule is `block.timestamp + (current delay - new delay)`.
```

### [Informational] glamsterdam-block-context

- **Location**: `access/extensions/IAccessControlDefaultAdminRules.sol:155`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
153:      * - When the delay is changed for a larger one the schedule is `block.timestamp + newDelay` capped by
154:      * {defaultAdminDelayIncreaseWait}.
155:      * - When the delay is changed for a shorter one, the schedule is `block.timestamp + (current delay - new delay)`.
156:      *
157:      * A {pendingDefaultAdminDelay} that never got into effect will be canceled in favor of a new scheduled change.
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `access/manager/AccessManager.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Rule confidence**: low
- **Rule rationale**: File size is a rough proxy for deployed bytecode size. A raised max contract size would relax rather than break constraints, so this is a watch point only.
- **Related fork candidates**: EIP-7907 (meter and increase contract code size, candidate)
- **Manual review required**: Yes

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `access/manager/AccessManager.sol:380`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
378:         uint64 roleId
379:     ) public virtual onlyAuthorized {
380:         for (uint256 i = 0; i < selectors.length; ++i) {
381:             _setTargetFunctionRole(target, selectors[i], roleId);
382:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `access/manager/AuthorityUtils.sol:22`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
20:         bytes memory data = abi.encodeCall(IAuthority.canCall, (caller, target, selector));
21: 
22:         assembly ("memory-safe") {
23:             mstore(0x00, 0x00)
24:             mstore(0x20, 0x00)
```

### [Informational] glamsterdam-block-context

- **Location**: `account/utils/draft-ERC4337Utils.sol:168`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
166:             validationData
167:         );
168:         uint256 current = Math.ternary(range == ValidationRange.TIMESTAMP, block.timestamp, block.number);
169:         return (aggregator_, current <= validAfter || validUntil < current);
170:     }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `account/utils/draft-ERC7579Utils.sol:85`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
83:         Execution[] calldata executionBatch = decodeBatch(executionCalldata);
84:         returnData = new bytes[](executionBatch.length);
85:         for (uint256 i = 0; i < executionBatch.length; ++i) {
86:             returnData[i] = _call(
87:                 i,
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `account/utils/draft-ERC7579Utils.sol:206`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
204:                 revert ERC7579DecodingError();
205: 
206:             assembly ("memory-safe") {
207:                 executionBatch.offset := add(add(executionCalldata.offset, arrayLengthOffset), 0x20)
208:                 executionBatch.length := arrayLength
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `account/utils/draft-ERC7579Utils.sol:221`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Rule confidence**: medium
- **Rule rationale**: transfer()/send() forward a fixed 2300 gas stipend and value-bearing calls embed gas-cost assumptions. Gas repricing candidates and native ETH transfer logs directly touch these patterns, so a keyword match is usually relevant.
- **Related fork candidates**: EIP-7708 (ETH transfers emit a log, candidate), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
219:         bytes calldata data
220:     ) private returns (bytes memory) {
221:         (bool success, bytes memory returndata) = (target == address(0) ? address(this) : target).call{value: value}(
222:             data
223:         );
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `account/utils/draft-ERC7579Utils.sol:234`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
232:         bytes calldata data
233:     ) private returns (bytes memory) {
234:         (bool success, bytes memory returndata) = (target == address(0) ? address(this) : target).delegatecall(data);
235:         return _validateExecutionMode(index, execType, success, returndata);
236:     }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `crosschain/CrosschainLinked.sol:47`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
45: 
46:     constructor(Link[] memory links) {
47:         for (uint256 i = 0; i < links.length; ++i) {
48:             _setLink(links[i].gateway, links[i].counterpart, false);
49:         }
```

### [Informational] glamsterdam-block-context

- **Location**: `finance/VestingWallet.sol:98`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
96:      */
97:     function releasable() public view virtual returns (uint256) {
98:         return vestedAmount(uint64(block.timestamp)) - released();
99:     }
100: 
```

### [Informational] glamsterdam-block-context

- **Location**: `finance/VestingWallet.sol:106`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
104:      */
105:     function releasable(address token) public view virtual returns (uint256) {
106:         return vestedAmount(token, uint64(block.timestamp)) - released(token);
107:     }
108: 
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `governance/Governor.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Rule confidence**: low
- **Rule rationale**: File size is a rough proxy for deployed bytecode size. A raised max contract size would relax rather than break constraints, so this is a watch point only.
- **Related fork candidates**: EIP-7907 (meter and increase contract code size, candidate)
- **Manual review required**: Yes

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/Governor.sol:222`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
220:             bytes32 msgDataHash = keccak256(_msgData());
221:             // loop until popping the expected operation - throw if deque is empty (operation not authorized)
222:             while (_governanceCall.popFront() != msgDataHash) {}
223:         }
224:     }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/Governor.sol:408`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
406:         // before execute: register governance call in queue.
407:         if (_executor() != address(this)) {
408:             for (uint256 i = 0; i < targets.length; ++i) {
409:                 if (targets[i] == address(this)) {
410:                     _governanceCall.pushBack(keccak256(calldatas[i]));
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/Governor.sol:441`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
439:         bytes32 /*descriptionHash*/
440:     ) internal virtual {
441:         for (uint256 i = 0; i < targets.length; ++i) {
442:             (bool success, bytes memory returndata) = targets[i].call{value: values[i]}(calldatas[i]);
443:             Address.verifyCallResult(success, returndata);
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `governance/Governor.sol:442`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Rule confidence**: medium
- **Rule rationale**: transfer()/send() forward a fixed 2300 gas stipend and value-bearing calls embed gas-cost assumptions. Gas repricing candidates and native ETH transfer logs directly touch these patterns, so a keyword match is usually relevant.
- **Related fork candidates**: EIP-7708 (ETH transfers emit a log, candidate), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
440:     ) internal virtual {
441:         for (uint256 i = 0; i < targets.length; ++i) {
442:             (bool success, bytes memory returndata) = targets[i].call{value: values[i]}(calldatas[i]);
443:             Address.verifyCallResult(success, returndata);
444:         }
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `governance/Governor.sol:657`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Rule confidence**: medium
- **Rule rationale**: transfer()/send() forward a fixed 2300 gas stipend and value-bearing calls embed gas-cost assumptions. Gas repricing candidates and native ETH transfer logs directly touch these patterns, so a keyword match is usually relevant.
- **Related fork candidates**: EIP-7708 (ETH transfers emit a log, candidate), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
655:      */
656:     function relay(address target, uint256 value, bytes calldata data) public payable virtual onlyGovernance {
657:         (bool success, bytes memory returndata) = target.call{value: value}(data);
658:         Address.verifyCallResult(success, returndata);
659:     }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `governance/Governor.sol:811`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
809:      *
810:      * NOTE: making this function internal would mean it could be used with memory unsafe offset, and marking the
811:      * assembly block as such would prevent some optimizations.
812:      */
813:     function _unsafeReadBytesOffset(bytes memory buffer, uint256 offset) private pure returns (bytes32 value) {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `governance/Governor.sol:815`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
813:     function _unsafeReadBytesOffset(bytes memory buffer, uint256 offset) private pure returns (bytes32 value) {
814:         // This is not memory safe in the general case, but all calls to this private function are within bounds.
815:         assembly ("memory-safe") {
816:             value := mload(add(add(buffer, 0x20), offset))
817:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/TimelockController.sol:125`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
123: 
124:         // register proposers and cancellers
125:         for (uint256 i = 0; i < proposers.length; ++i) {
126:             _grantRole(PROPOSER_ROLE, proposers[i]);
127:             _grantRole(CANCELLER_ROLE, proposers[i]);
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/TimelockController.sol:131`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
129: 
130:         // register executors
131:         for (uint256 i = 0; i < executors.length; ++i) {
132:             _grantRole(EXECUTOR_ROLE, executors[i]);
133:         }
```

### [Informational] glamsterdam-block-context

- **Location**: `governance/TimelockController.sol:211`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
209:         } else if (timestamp == DONE_TIMESTAMP) {
210:             return OperationState.Done;
211:         } else if (timestamp > block.timestamp) {
212:             return OperationState.Waiting;
213:         } else {
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/TimelockController.sol:303`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
301:         bytes32 id = hashOperationBatch(targets, values, payloads, predecessor, salt);
302:         _schedule(id, delay);
303:         for (uint256 i = 0; i < targets.length; ++i) {
304:             emit CallScheduled(id, i, targets[i], values[i], payloads[i], predecessor, delay);
305:         }
```

### [Informational] glamsterdam-block-context

- **Location**: `governance/TimelockController.sol:322`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
320:             revert TimelockInsufficientDelay(delay, minDelay);
321:         }
322:         _timestamps[id] = block.timestamp + delay;
323:     }
324: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/TimelockController.sol:397`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
395: 
396:         _beforeCall(id, predecessor);
397:         for (uint256 i = 0; i < targets.length; ++i) {
398:             address target = targets[i];
399:             uint256 value = values[i];
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `governance/TimelockController.sol:411`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Rule confidence**: medium
- **Rule rationale**: transfer()/send() forward a fixed 2300 gas stipend and value-bearing calls embed gas-cost assumptions. Gas repricing candidates and native ETH transfer logs directly touch these patterns, so a keyword match is usually relevant.
- **Related fork candidates**: EIP-7708 (ETH transfers emit a log, candidate), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
409:      */
410:     function _execute(address target, uint256 value, bytes calldata data) internal virtual {
411:         (bool success, bytes memory returndata) = target.call{value: value}(data);
412:         Address.verifyCallResult(success, returndata);
413:     }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `governance/extensions/GovernorCountingFractional.sol:166`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
164:             if (params.length != 0x30) revert GovernorInvalidVoteParams();
165: 
166:             assembly ("memory-safe") {
167:                 againstVotes := shr(128, mload(add(params, 0x20)))
168:                 forVotes := shr(128, mload(add(params, 0x30)))
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/extensions/GovernorTimelockAccess.sol:135`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
133:         bool ignored
134:     ) public virtual onlyGovernance {
135:         for (uint256 i = 0; i < selectors.length; ++i) {
136:             _setAccessManagerIgnored(target, selectors[i], ignored);
137:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/extensions/GovernorTimelockAccess.sol:167`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
165:         indirect = new bool[](length);
166:         withDelay = new bool[](length);
167:         for (uint256 i = 0; i < length; ++i) {
168:             (indirect[i], withDelay[i], ) = _getManagerData(plan, i);
169:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/extensions/GovernorTimelockAccess.sol:193`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
191:         plan.length = SafeCast.toUint16(targets.length);
192: 
193:         for (uint256 i = 0; i < targets.length; ++i) {
194:             if (calldatas[i].length < 4) {
195:                 continue;
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/extensions/GovernorTimelockAccess.sol:233`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
231:         uint48 etaSeconds = Time.timestamp() + plan.delay;
232: 
233:         for (uint256 i = 0; i < targets.length; ++i) {
234:             (, bool withDelay, ) = _getManagerData(plan, i);
235:             if (withDelay) {
```

### [Informational] glamsterdam-block-context

- **Location**: `governance/extensions/GovernorTimelockAccess.sol:258`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
256:     ) internal virtual override {
257:         uint48 etaSeconds = SafeCast.toUint48(proposalEta(proposalId));
258:         if (block.timestamp < etaSeconds) {
259:             revert GovernorUnmetDelay(proposalId, etaSeconds);
260:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/extensions/GovernorTimelockAccess.sol:264`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
262:         ExecutionPlan storage plan = _executionPlan[proposalId];
263: 
264:         for (uint256 i = 0; i < targets.length; ++i) {
265:             (bool controlled, bool withDelay, uint32 nonce) = _getManagerData(plan, i);
266:             if (controlled) {
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `governance/extensions/GovernorTimelockAccess.sol:272`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Rule confidence**: medium
- **Rule rationale**: transfer()/send() forward a fixed 2300 gas stipend and value-bearing calls embed gas-cost assumptions. Gas repricing candidates and native ETH transfer logs directly touch these patterns, so a keyword match is usually relevant.
- **Related fork candidates**: EIP-7708 (ETH transfers emit a log, candidate), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
270:                 }
271:             } else {
272:                 (bool success, bytes memory returndata) = targets[i].call{value: values[i]}(calldatas[i]);
273:                 Address.verifyCallResult(success, returndata);
274:             }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/extensions/GovernorTimelockAccess.sol:293`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
291:         // If the proposal has been scheduled it will have an ETA and we may have to externally cancel
292:         if (etaSeconds != 0) {
293:             for (uint256 i = 0; i < targets.length; ++i) {
294:                 (, bool withDelay, uint32 nonce) = _getManagerData(plan, i);
295:                 // Only attempt to cancel if the execution plan included a delay
```

### [Informational] glamsterdam-block-context

- **Location**: `governance/extensions/GovernorTimelockCompound.sol:44`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
42:         return
43:             (currentState == ProposalState.Queued &&
44:                 block.timestamp >= proposalEta(proposalId) + _timelock.GRACE_PERIOD())
45:                 ? ProposalState.Expired
46:                 : currentState;
```

### [Informational] glamsterdam-block-context

- **Location**: `governance/extensions/GovernorTimelockCompound.sol:71`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
69:         bytes32 /*descriptionHash*/
70:     ) internal virtual override returns (uint48) {
71:         uint48 etaSeconds = SafeCast.toUint48(block.timestamp + _timelock.delay());
72: 
73:         for (uint256 i = 0; i < targets.length; ++i) {
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/extensions/GovernorTimelockCompound.sol:73`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
71:         uint48 etaSeconds = SafeCast.toUint48(block.timestamp + _timelock.delay());
72: 
73:         for (uint256 i = 0; i < targets.length; ++i) {
74:             if (
75:                 _timelock.queuedTransactions(keccak256(abi.encode(targets[i], values[i], "", calldatas[i], etaSeconds)))
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/extensions/GovernorTimelockCompound.sol:101`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
99:         }
100:         Address.sendValue(payable(_timelock), msg.value);
101:         for (uint256 i = 0; i < targets.length; ++i) {
102:             _timelock.executeTransaction(targets[i], values[i], "", calldatas[i], etaSeconds);
103:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `governance/extensions/GovernorTimelockCompound.sol:121`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
119:         if (etaSeconds > 0) {
120:             // do external call later
121:             for (uint256 i = 0; i < targets.length; ++i) {
122:                 _timelock.cancelTransaction(targets[i], values[i], "", calldatas[i], etaSeconds);
123:             }
```

### [Informational] glamsterdam-block-context

- **Location**: `governance/extensions/GovernorTimelockControl.sol:90`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
88:         _timelock.scheduleBatch(targets, values, calldatas, 0, salt, delay);
89: 
90:         return SafeCast.toUint48(block.timestamp + delay);
91:     }
92: 
```

### [Informational] glamsterdam-block-context

- **Location**: `governance/utils/Votes.sol:152`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
150:         bytes32 s
151:     ) public virtual {
152:         if (block.timestamp > expiry) {
153:             revert VotesExpiredSignature(expiry);
154:         }
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `governance/utils/VotesExtended.sol:23`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Rule confidence**: medium
- **Rule rationale**: transfer()/send() forward a fixed 2300 gas stipend and value-bearing calls embed gas-cost assumptions. Gas repricing candidates and native ETH transfer logs directly touch these patterns, so a keyword match is usually relevant.
- **Related fork candidates**: EIP-7708 (ETH transfers emit a log, candidate), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
21:  * contract VotingToken is Token, VotesExtended {
22:  *   function transfer(address from, address to, uint256 tokenId) public override {
23:  *     super.transfer(from, to, tokenId); // <- Perform the transfer first ...
24:  *     _transferVotingUnits(from, to, 1); // <- ... then call _transferVotingUnits.
25:  *   }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `metatx/ERC2771Forwarder.sol:172`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
170:         uint256 refundValue;
171: 
172:         for (uint256 i; i < requests.length; ++i) {
173:             requestsValue += requests[i].value;
174:             bool success = _execute(requests[i], atomic);
```

### [Informational] glamsterdam-block-context

- **Location**: `metatx/ERC2771Forwarder.sol:207`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
205:         return (
206:             _isTrustedByTarget(request.to),
207:             request.deadline >= block.timestamp,
208:             isValid && recovered == request.from,
209:             recovered
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `metatx/ERC2771Forwarder.sol:289`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
287:             uint256 gasLeft;
288: 
289:             assembly ("memory-safe") {
290:                 success := call(reqGas, to, value, add(data, 0x20), mload(data), 0x00, 0x00)
291:                 gasLeft := gas()
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `metatx/ERC2771Forwarder.sol:315`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
313:         uint256 returnSize;
314:         uint256 returnValue;
315:         assembly ("memory-safe") {
316:             // Perform the staticcall and save the result in the scratch space.
317:             // | Location  | Content  | Content (Hex)                                                      |
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `metatx/ERC2771Forwarder.sol:367`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
365:             // neither revert or assert consume all gas since Solidity 0.8.20
366:             // https://docs.soliditylang.org/en/v0.8.20/control-structures.html#panic-via-assert-and-error-via-require
367:             assembly ("memory-safe") {
368:                 invalid()
369:             }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `mocks/BatchCaller.sol:15`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
13:     function execute(Call[] calldata calls) external returns (bytes[] memory) {
14:         bytes[] memory returndata = new bytes[](calls.length);
15:         for (uint256 i = 0; i < calls.length; ++i) {
16:             returndata[i] = Address.functionCallWithValue(calls[i].target, calls[i].data, calls[i].value);
17:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/CallReceiverMock.sol:18`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
16: 
17:     function mockFunctionWritesStorage(bytes32 slot, bytes32 value) public returns (string memory) {
18:         assembly ("memory-safe") {
19:             sstore(slot, value)
20:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/CallReceiverMock.sol:29`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
27: 
28:     function mockFunctionEmptyReturnWritesStorage(bytes32 slot, bytes32 value) public payable {
29:         assembly ("memory-safe") {
30:             sstore(slot, value)
31:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/CallReceiverMock.sol:52`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
50:         uint256 b
51:     ) public payable returns (uint256, uint256) {
52:         assembly ("memory-safe") {
53:             sstore(slot, value)
54:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `mocks/CallReceiverMock.sol:86`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
84: 
85:     function mockFunctionOutOfGas() public payable {
86:         for (uint256 i = 0; ; ++i) {
87:             _array.push(i);
88:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/ERC1271WalletMock.sol:19`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
17: contract ERC1271MaliciousMock is IERC1271 {
18:     function isValidSignature(bytes32, bytes memory) public pure returns (bytes4) {
19:         assembly {
20:             mstore(0, 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)
21:             return(0, 32)
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `mocks/ERC165Mock.sol:54`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
52: contract ERC165InterfacesSupported is SupportsInterfaceWithLookupMock {
53:     constructor(bytes4[] memory interfaceIds) {
54:         for (uint256 i = 0; i < interfaceIds.length; i++) {
55:             _registerInterface(interfaceIds[i]);
56:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `mocks/ERC165Mock.sol:63`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
61: contract ERC165RevertInvalid is SupportsInterfaceWithLookupMock {
62:     constructor(bytes4[] memory interfaceIds) {
63:         for (uint256 i = 0; i < interfaceIds.length; i++) {
64:             _registerInterface(interfaceIds[i]);
65:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/ERC165Mock.sol:76`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
74: contract ERC165MaliciousData {
75:     function supportsInterface(bytes4) public pure returns (bool) {
76:         assembly {
77:             mstore(0, 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff)
78:             return(0, 32)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/ERC165Mock.sol:92`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
90:     function supportsInterface(bytes4 interfaceId) public pure override returns (bool) {
91:         if (interfaceId == type(IERC165).interfaceId) {
92:             assembly {
93:                 mstore(0, 1)
94:             }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/ERC165Mock.sol:96`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
94:             }
95:         }
96:         assembly {
97:             return(0, 101500)
98:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `mocks/MulticallHelper.sol:14`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
12:     ) external {
13:         bytes[] memory calls = new bytes[](recipients.length);
14:         for (uint256 i = 0; i < recipients.length; i++) {
15:             calls[i] = abi.encodeCall(multicallToken.transfer, (recipients[i], amounts[i]));
16:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `mocks/MulticallHelper.sol:19`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
17: 
18:         bytes[] memory results = multicallToken.multicall(calls);
19:         for (uint256 i = 0; i < results.length; i++) {
20:             require(abi.decode(results[i], (bool)));
21:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/ReentrancyAttack.sol:9`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
7: contract ReentrancyAttack is Context {
8:     function callSender(bytes calldata data) public {
9:         (bool success, ) = _msgSender().call(data);
10:         require(success, "ReentrancyAttack: failed call");
11:     }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/ReentrancyAttack.sol:14`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
12: 
13:     function staticcallSender(bytes calldata data) public view {
14:         (bool success, ) = _msgSender().staticcall(data);
15:         require(success, "ReentrancyAttack: failed call");
16:     }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/ReentrancyMock.sol:33`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
31:         if (n > 0) {
32:             _count();
33:             (bool success, ) = address(this).call(abi.encodeCall(this.countThisRecursive, (n - 1)));
34:             require(success, "ReentrancyMock: failed call");
35:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/ReentrancyTransientMock.sol:33`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
31:         if (n > 0) {
32:             _count();
33:             (bool success, ) = address(this).call(abi.encodeCall(this.countThisRecursive, (n - 1)));
34:             require(success, "ReentrancyTransientMock: failed call");
35:         }
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/VotesExtendedMock.sol:35`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
33: abstract contract VotesExtendedTimestampMock is VotesExtendedMock {
34:     function clock() public view override returns (uint48) {
35:         return uint48(block.timestamp);
36:     }
37: 
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/VotesMock.sol:35`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
33: abstract contract VotesTimestampMock is VotesMock {
34:     function clock() public view override returns (uint48) {
35:         return uint48(block.timestamp);
36:     }
37: 
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `mocks/compound/CompTimelock.sol:162`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Rule confidence**: medium
- **Rule rationale**: transfer()/send() forward a fixed 2300 gas stipend and value-bearing calls embed gas-cost assumptions. Gas repricing candidates and native ETH transfer logs directly touch these patterns, so a keyword match is usually relevant.
- **Related fork candidates**: EIP-7708 (ETH transfers emit a log, candidate), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
160: 
161:         // solium-disable-next-line security/no-call-value
162:         (bool success, bytes memory returnData) = target.call{value: value}(callData);
163:         require(success, "Timelock::executeTransaction: Transaction execution reverted.");
164: 
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/compound/CompTimelock.sol:172`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
170:     function getBlockTimestamp() internal view returns (uint256) {
171:         // solium-disable-next-line security/no-block-members
172:         return block.timestamp;
173:     }
174: }
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/docs/ERC20WithAutoMinerReward.sol:13`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
11: 
12:     function _mintMinerReward() internal {
13:         _mint(block.coinbase, 1000);
14:     }
15: 
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/docs/ERC20WithAutoMinerReward.sol:17`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
15: 
16:     function _update(address from, address to, uint256 value) internal virtual override {
17:         if (!(from == address(0) && to == block.coinbase)) {
18:             _mintMinerReward();
19:         }
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/docs/governance/MyTokenTimestampBased.sol:15`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
13: 
14:     function clock() public view override returns (uint48) {
15:         return uint48(block.timestamp);
16:     }
17: 
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/token/ERC1363NoReturnMock.sol:10`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
8:     function transferAndCall(address to, uint256 value, bytes memory data) public override returns (bool) {
9:         super.transferAndCall(to, value, data);
10:         assembly {
11:             return(0, 0)
12:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/token/ERC1363NoReturnMock.sol:22`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
20:     ) public override returns (bool) {
21:         super.transferFromAndCall(from, to, value, data);
22:         assembly {
23:             return(0, 0)
24:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/token/ERC1363NoReturnMock.sol:29`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
27:     function approveAndCall(address spender, uint256 value, bytes memory data) public override returns (bool) {
28:         super.approveAndCall(spender, value, data);
29:         assembly {
30:             return(0, 0)
31:         }
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `mocks/token/ERC20NoReturnMock.sol:10`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Rule confidence**: medium
- **Rule rationale**: transfer()/send() forward a fixed 2300 gas stipend and value-bearing calls embed gas-cost assumptions. Gas repricing candidates and native ETH transfer logs directly touch these patterns, so a keyword match is usually relevant.
- **Related fork candidates**: EIP-7708 (ETH transfers emit a log, candidate), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
8:     function transfer(address to, uint256 amount) public override returns (bool) {
9:         // forge-lint: disable-next-line(erc20-unchecked-transfer)
10:         super.transfer(to, amount);
11:         assembly {
12:             return(0, 0)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/token/ERC20NoReturnMock.sol:11`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
9:         // forge-lint: disable-next-line(erc20-unchecked-transfer)
10:         super.transfer(to, amount);
11:         assembly {
12:             return(0, 0)
13:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/token/ERC20NoReturnMock.sol:19`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
17:         // forge-lint: disable-next-line(erc20-unchecked-transfer)
18:         super.transferFrom(from, to, amount);
19:         assembly {
20:             return(0, 0)
21:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/token/ERC20NoReturnMock.sol:26`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
24:     function approve(address spender, uint256 amount) public override returns (bool) {
25:         super.approve(spender, amount);
26:         assembly {
27:             return(0, 0)
28:         }
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/token/ERC20VotesAdditionalCheckpointsMock.sol:24`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
22: abstract contract ERC20VotesExtendedTimestampMock is ERC20VotesExtendedMock {
23:     function clock() public view virtual override returns (uint48) {
24:         return SafeCast.toUint48(block.timestamp);
25:     }
26: 
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/token/ERC20VotesLegacyMock.sol:66`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
64:      */
65:     function getPastVotes(address account, uint256 blockNumber) public view virtual returns (uint256) {
66:         require(blockNumber < block.number, "ERC20Votes: block not yet mined");
67:         return _checkpointsLookup(_checkpoints[account], blockNumber);
68:     }
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/token/ERC20VotesLegacyMock.sol:79`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
77:      */
78:     function getPastTotalSupply(uint256 blockNumber) public view virtual returns (uint256) {
79:         require(blockNumber < block.number, "ERC20Votes: block not yet mined");
80:         return _checkpointsLookup(_totalSupplyCheckpoints, blockNumber);
81:     }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `mocks/token/ERC20VotesLegacyMock.sol:114`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
112:         }
113: 
114:         while (low < high) {
115:             uint256 mid = Math.average(low, high);
116:             if (_unsafeAccess(ckpts, mid).fromBlock > blockNumber) {
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/token/ERC20VotesLegacyMock.sol:146`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
144:         bytes32 s
145:     ) public virtual {
146:         require(block.timestamp <= expiry, "ERC20Votes: signature expired");
147:         address signer = ECDSA.recover(
148:             _hashTypedDataV4(keccak256(abi.encode(_DELEGATION_TYPEHASH, delegatee, nonce, expiry))),
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/token/ERC20VotesLegacyMock.sol:226`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
224:             newWeight = op(oldWeight, delta);
225: 
226:             if (pos > 0 && oldCkpt.fromBlock == block.number) {
227:                 _unsafeAccess(ckpts, pos - 1).votes = SafeCast.toUint224(newWeight);
228:             } else {
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/token/ERC20VotesLegacyMock.sol:230`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
228:             } else {
229:                 ckpts.push(
230:                     Checkpoint({fromBlock: SafeCast.toUint32(block.number), votes: SafeCast.toUint224(newWeight)})
231:                 );
232:             }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `mocks/token/ERC20VotesLegacyMock.sol:248`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
246:      */
247:     function _unsafeAccess(Checkpoint[] storage ckpts, uint256 pos) private pure returns (Checkpoint storage result) {
248:         assembly {
249:             mstore(0, ckpts.slot)
250:             result.slot := add(keccak256(0, 0x20), pos)
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/token/ERC20VotesTimestampMock.sol:11`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
9: abstract contract ERC20VotesTimestampMock is ERC20Votes {
10:     function clock() public view virtual override returns (uint48) {
11:         return SafeCast.toUint48(block.timestamp);
12:     }
13: 
```

### [Informational] glamsterdam-block-context

- **Location**: `mocks/token/ERC20VotesTimestampMock.sol:22`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
20: abstract contract ERC721VotesTimestampMock is ERC721Votes {
21:     function clock() public view virtual override returns (uint48) {
22:         return SafeCast.toUint48(block.timestamp);
23:     }
24: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `mocks/token/ERC721ConsecutiveEnumerableMock.sol:16`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
14:         uint96[] memory amounts
15:     ) ERC721(name, symbol) {
16:         for (uint256 i = 0; i < receivers.length; ++i) {
17:             _mintConsecutive(receivers[i], amounts[i]);
18:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `mocks/token/ERC721ConsecutiveMock.sol:27`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
25:         _offset = offset;
26: 
27:         for (uint256 i = 0; i < delegates.length; ++i) {
28:             _delegate(delegates[i], delegates[i]);
29:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `mocks/token/ERC721ConsecutiveMock.sol:31`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
29:         }
30: 
31:         for (uint256 i = 0; i < receivers.length; ++i) {
32:             _mintConsecutive(receivers[i], amounts[i]);
33:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `proxy/Clones.sol:51`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
49:             revert Errors.InsufficientBalance(address(this).balance, value);
50:         }
51:         assembly ("memory-safe") {
52:             // Cleans the upper 96 bits of the `implementation` word, then packs the first 3 bytes
53:             // of the `implementation` address with the bytecode before the address.
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `proxy/Clones.sol:98`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
96:             revert Errors.InsufficientBalance(address(this).balance, value);
97:         }
98:         assembly ("memory-safe") {
99:             // Cleans the upper 96 bits of the `implementation` word, then packs the first 3 bytes
100:             // of the `implementation` address with the bytecode before the address.
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `proxy/Clones.sol:119`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
117:         address deployer
118:     ) internal pure returns (address predicted) {
119:         assembly ("memory-safe") {
120:             let ptr := mload(0x40)
121:             mstore(add(ptr, 0x38), deployer)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `proxy/Clones.sol:176`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
174:         }
175:         bytes memory bytecode = _cloneCodeWithImmutableArgs(implementation, args);
176:         assembly ("memory-safe") {
177:             instance := create(value, add(bytecode, 0x20), mload(bytecode))
178:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `proxy/Clones.sol:263`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
261:     function fetchCloneArgs(address instance) internal view returns (bytes memory) {
262:         bytes memory result = new bytes(instance.code.length - 0x2d); // revert if length is too short
263:         assembly ("memory-safe") {
264:             extcodecopy(instance, add(result, 0x20), 0x2d, mload(result))
265:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `proxy/Clones.sol:272`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
270:      * @dev Helper that prepares the initcode of the proxy with immutable args.
271:      *
272:      * An assembly variant of this function requires copying the `args` array, which can be efficiently done using
273:      * `mcopy`. Unfortunately, that opcode is not available before cancun. A pure solidity implementation using
274:      * abi.encodePacked is more expensive but also more portable and easier to review.
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `proxy/Proxy.sol:23`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
21:      */
22:     function _delegate(address implementation) internal virtual {
23:         assembly {
24:             // Copy msg.data. We take full control of memory in this inline assembly
25:             // block because it will not return to Solidity code. We overwrite the
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `proxy/utils/Initializable.sol:234`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
232:     function _getInitializableStorage() private pure returns (InitializableStorage storage $) {
233:         bytes32 slot = _initializableStorageSlot();
234:         assembly {
235:             $.slot := slot
236:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `token/ERC1155/ERC1155.sol:81`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
79:         uint256[] memory batchBalances = new uint256[](accounts.length);
80: 
81:         for (uint256 i = 0; i < accounts.length; ++i) {
82:             batchBalances[i] = balanceOf(accounts.unsafeMemoryAccess(i), ids.unsafeMemoryAccess(i));
83:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `token/ERC1155/ERC1155.sol:144`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
142:         address operator = _msgSender();
143: 
144:         for (uint256 i = 0; i < ids.length; ++i) {
145:             uint256 id = ids.unsafeMemoryAccess(i);
146:             uint256 value = values.unsafeMemoryAccess(i);
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `token/ERC1155/ERC1155.sol:400`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
398:         uint256 element2
399:     ) private pure returns (uint256[] memory array1, uint256[] memory array2) {
400:         assembly ("memory-safe") {
401:             // Load the free memory pointer
402:             array1 := mload(0x40)
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `token/ERC1155/extensions/ERC1155Supply.sol:60`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
58:         if (from == address(0)) {
59:             uint256 totalMintValue = 0;
60:             for (uint256 i = 0; i < ids.length; ++i) {
61:                 uint256 value = values.unsafeMemoryAccess(i);
62:                 // Overflow check required: The rest of the code assumes that totalSupply never overflows
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `token/ERC1155/extensions/ERC1155Supply.sol:72`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
70:         if (to == address(0)) {
71:             uint256 totalBurnValue = 0;
72:             for (uint256 i = 0; i < ids.length; ++i) {
73:                 uint256 value = values.unsafeMemoryAccess(i);
74: 
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `token/ERC1155/utils/ERC1155Utils.sol:44`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
42:                     revert IERC1155Errors.ERC1155InvalidReceiver(to);
43:                 } else {
44:                     assembly ("memory-safe") {
45:                         revert(add(reason, 0x20), mload(reason))
46:                     }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `token/ERC1155/utils/ERC1155Utils.sol:81`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
79:                     revert IERC1155Errors.ERC1155InvalidReceiver(to);
80:                 } else {
81:                     assembly ("memory-safe") {
82:                         revert(add(reason, 0x20), mload(reason))
83:                     }
```

### [Informational] glamsterdam-block-context

- **Location**: `token/ERC20/extensions/ERC20Permit.sol:51`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
49:         bytes32 s
50:     ) public virtual {
51:         if (block.timestamp > deadline) {
52:             revert ERC2612ExpiredSignature(deadline);
53:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `token/ERC20/utils/ERC1363Utils.sol:55`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
53:                 revert ERC1363InvalidReceiver(to);
54:             } else {
55:                 assembly ("memory-safe") {
56:                     revert(add(reason, 0x20), mload(reason))
57:                 }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `token/ERC20/utils/ERC1363Utils.sol:89`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
87:                 revert ERC1363InvalidSpender(spender);
88:             } else {
89:                 assembly ("memory-safe") {
90:                     revert(add(reason, 0x20), mload(reason))
91:                 }
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `token/ERC20/utils/SafeERC20.sol:168`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Rule confidence**: medium
- **Rule rationale**: transfer()/send() forward a fixed 2300 gas stipend and value-bearing calls embed gas-cost assumptions. Gas repricing candidates and native ETH transfer logs directly touch these patterns, so a keyword match is usually relevant.
- **Related fork candidates**: EIP-7708 (ETH transfers emit a log, candidate), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
166: 
167:     /**
168:      * @dev Imitates a Solidity `token.transfer(to, value)` call, relaxing the requirement on the return value: the
169:      * return value is optional (but if data is returned, it must not be false).
170:      *
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `token/ERC20/utils/SafeERC20.sol:179`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
177:         bytes4 selector = IERC20.transfer.selector;
178: 
179:         assembly ("memory-safe") {
180:             let fmp := mload(0x40)
181:             mstore(0x00, selector)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `token/ERC20/utils/SafeERC20.sol:221`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
219:         bytes4 selector = IERC20.transferFrom.selector;
220: 
221:         assembly ("memory-safe") {
222:             let fmp := mload(0x40)
223:             mstore(0x00, selector)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `token/ERC20/utils/SafeERC20.sol:258`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
256:         bytes4 selector = IERC20.approve.selector;
257: 
258:         assembly ("memory-safe") {
259:             let fmp := mload(0x40)
260:             mstore(0x00, selector)
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `token/ERC721/extensions/ERC721Wrapper.sol:33`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
31:     function depositFor(address account, uint256[] memory tokenIds) public virtual returns (bool) {
32:         uint256 length = tokenIds.length;
33:         for (uint256 i = 0; i < length; ++i) {
34:             uint256 tokenId = tokenIds[i];
35: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `token/ERC721/extensions/ERC721Wrapper.sol:51`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
49:     function withdrawTo(address account, uint256[] memory tokenIds) public virtual returns (bool) {
50:         uint256 length = tokenIds.length;
51:         for (uint256 i = 0; i < length; ++i) {
52:             uint256 tokenId = tokenIds[i];
53:             // Setting an "auth" arguments enables the `_isAuthorized` check which verifies that the token exists
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `token/ERC721/utils/ERC721Utils.sol:43`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
41:                     revert IERC721Errors.ERC721InvalidReceiver(to);
42:                 } else {
43:                     assembly ("memory-safe") {
44:                         revert(add(reason, 0x20), mload(reason))
45:                     }
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `utils/Arrays.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Rule confidence**: low
- **Rule rationale**: File size is a rough proxy for deployed bytecode size. A raised max contract size would relax rather than break constraints, so this is a watch point only.
- **Related fork candidates**: EIP-7907 (meter and increase contract code size, candidate)
- **Manual review required**: Yes

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Arrays.sol:124`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
122:             uint256 pos = begin;
123: 
124:             for (uint256 it = begin + 0x20; it < end; it += 0x20) {
125:                 if (comp(_mload(it), pivot)) {
126:                     // If the value stored at the iterator's position comes before the pivot, we increment the
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:143`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
141:      */
142:     function _begin(uint256[] memory array) private pure returns (uint256 ptr) {
143:         assembly ("memory-safe") {
144:             ptr := add(array, 0x20)
145:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:162`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
160:      */
161:     function _mload(uint256 ptr) private pure returns (uint256 value) {
162:         assembly {
163:             value := mload(ptr)
164:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:171`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
169:      */
170:     function _swap(uint256 ptr1, uint256 ptr2) private pure {
171:         assembly {
172:             let value1 := mload(ptr1)
173:             let value2 := mload(ptr2)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:181`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
179:     /// @dev Helper: low level cast address memory array to uint256 memory array
180:     function _castToUint256Array(address[] memory input) private pure returns (uint256[] memory output) {
181:         assembly {
182:             output := input
183:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:188`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
186:     /// @dev Helper: low level cast bytes32 memory array to uint256 memory array
187:     function _castToUint256Array(bytes32[] memory input) private pure returns (uint256[] memory output) {
188:         assembly {
189:             output := input
190:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:197`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
195:         function(address, address) pure returns (bool) input
196:     ) private pure returns (function(uint256, uint256) pure returns (bool) output) {
197:         assembly {
198:             output := input
199:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:206`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
204:         function(bytes32, bytes32) pure returns (bool) input
205:     ) private pure returns (function(uint256, uint256) pure returns (bool) output) {
206:         assembly {
207:             output := input
208:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Arrays.sol:232`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
230:         }
231: 
232:         while (low < high) {
233:             uint256 mid = Math.average(low, high);
234: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Arrays.sol:268`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
266:         }
267: 
268:         while (low < high) {
269:             uint256 mid = Math.average(low, high);
270: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Arrays.sol:302`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
300:         }
301: 
302:         while (low < high) {
303:             uint256 mid = Math.average(low, high);
304: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Arrays.sol:331`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
329:         }
330: 
331:         while (low < high) {
332:             uint256 mid = Math.average(low, high);
333: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Arrays.sol:360`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
358:         }
359: 
360:         while (low < high) {
361:             uint256 mid = Math.average(low, high);
362: 
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:401`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
399:         // allocate and copy
400:         address[] memory result = new address[](end - start);
401:         assembly ("memory-safe") {
402:             mcopy(add(result, 0x20), add(add(array, 0x20), mul(start, 0x20)), mul(sub(end, start), 0x20))
403:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:431`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
429:         // allocate and copy
430:         bytes32[] memory result = new bytes32[](end - start);
431:         assembly ("memory-safe") {
432:             mcopy(add(result, 0x20), add(add(array, 0x20), mul(start, 0x20)), mul(sub(end, start), 0x20))
433:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:461`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
459:         // allocate and copy
460:         uint256[] memory result = new uint256[](end - start);
461:         assembly ("memory-safe") {
462:             mcopy(add(result, 0x20), add(add(array, 0x20), mul(start, 0x20)), mul(sub(end, start), 0x20))
463:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:491`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
489: 
490:         // move and resize
491:         assembly ("memory-safe") {
492:             mcopy(add(array, 0x20), add(add(array, 0x20), mul(start, 0x20)), mul(sub(end, start), 0x20))
493:             mstore(array, sub(end, start))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:539`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
537: 
538:         // replace
539:         assembly ("memory-safe") {
540:             mcopy(
541:                 add(add(array, 0x20), mul(pos, 0x20)),
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:573`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
571: 
572:         // move and resize
573:         assembly ("memory-safe") {
574:             mcopy(add(array, 0x20), add(add(array, 0x20), mul(start, 0x20)), mul(sub(end, start), 0x20))
575:             mstore(array, sub(end, start))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:621`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
619: 
620:         // replace
621:         assembly ("memory-safe") {
622:             mcopy(
623:                 add(add(array, 0x20), mul(pos, 0x20)),
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:655`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
653: 
654:         // move and resize
655:         assembly ("memory-safe") {
656:             mcopy(add(array, 0x20), add(add(array, 0x20), mul(start, 0x20)), mul(sub(end, start), 0x20))
657:             mstore(array, sub(end, start))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:703`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
701: 
702:         // replace
703:         assembly ("memory-safe") {
704:             mcopy(
705:                 add(add(array, 0x20), mul(pos, 0x20)),
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:721`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
719:     function unsafeAccess(address[] storage arr, uint256 pos) internal pure returns (StorageSlot.AddressSlot storage) {
720:         bytes32 slot;
721:         assembly ("memory-safe") {
722:             slot := arr.slot
723:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:734`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
732:     function unsafeAccess(bytes32[] storage arr, uint256 pos) internal pure returns (StorageSlot.Bytes32Slot storage) {
733:         bytes32 slot;
734:         assembly ("memory-safe") {
735:             slot := arr.slot
736:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:747`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
745:     function unsafeAccess(uint256[] storage arr, uint256 pos) internal pure returns (StorageSlot.Uint256Slot storage) {
746:         bytes32 slot;
747:         assembly ("memory-safe") {
748:             slot := arr.slot
749:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:760`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
758:     function unsafeAccess(bytes[] storage arr, uint256 pos) internal pure returns (StorageSlot.BytesSlot storage) {
759:         bytes32 slot;
760:         assembly ("memory-safe") {
761:             slot := arr.slot
762:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:773`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
771:     function unsafeAccess(string[] storage arr, uint256 pos) internal pure returns (StorageSlot.StringSlot storage) {
772:         bytes32 slot;
773:         assembly ("memory-safe") {
774:             slot := arr.slot
775:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:785`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
783:      */
784:     function unsafeMemoryAccess(address[] memory arr, uint256 pos) internal pure returns (address res) {
785:         assembly {
786:             res := mload(add(add(arr, 0x20), mul(pos, 0x20)))
787:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:796`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
794:      */
795:     function unsafeMemoryAccess(bytes32[] memory arr, uint256 pos) internal pure returns (bytes32 res) {
796:         assembly {
797:             res := mload(add(add(arr, 0x20), mul(pos, 0x20)))
798:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:807`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
805:      */
806:     function unsafeMemoryAccess(uint256[] memory arr, uint256 pos) internal pure returns (uint256 res) {
807:         assembly {
808:             res := mload(add(add(arr, 0x20), mul(pos, 0x20)))
809:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:818`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
816:      */
817:     function unsafeMemoryAccess(bytes[] memory arr, uint256 pos) internal pure returns (bytes memory res) {
818:         assembly {
819:             res := mload(add(add(arr, 0x20), mul(pos, 0x20)))
820:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:829`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
827:      */
828:     function unsafeMemoryAccess(string[] memory arr, uint256 pos) internal pure returns (string memory res) {
829:         assembly {
830:             res := mload(add(add(arr, 0x20), mul(pos, 0x20)))
831:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:840`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
838:      */
839:     function unsafeSetLength(address[] storage array, uint256 len) internal {
840:         assembly ("memory-safe") {
841:             sstore(array.slot, len)
842:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:851`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
849:      */
850:     function unsafeSetLength(bytes32[] storage array, uint256 len) internal {
851:         assembly ("memory-safe") {
852:             sstore(array.slot, len)
853:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:862`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
860:      */
861:     function unsafeSetLength(uint256[] storage array, uint256 len) internal {
862:         assembly ("memory-safe") {
863:             sstore(array.slot, len)
864:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:873`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
871:      */
872:     function unsafeSetLength(bytes[] storage array, uint256 len) internal {
873:         assembly ("memory-safe") {
874:             sstore(array.slot, len)
875:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Arrays.sol:884`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
882:      */
883:     function unsafeSetLength(string[] storage array, uint256 len) internal {
884:         assembly ("memory-safe") {
885:             sstore(array.slot, len)
886:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Base58.sol:43`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
41:         if (inputLength == 0) return "";
42: 
43:         assembly ("memory-safe") {
44:             // Count number of zero bytes at the beginning of `input`. These are encoded using the same number of '1's
45:             // at the beginning of the encoded string.
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Base58.sol:147`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
145:         if (inputLength == 0) return "";
146: 
147:         assembly ("memory-safe") {
148:             let inputLeadingZeros := 0 // Number of leading '1' in `input`.
149:             // Count leading zeros. In base58, zeros are represented using '1' (chr(49)).
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Base64.sol:72`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
70:         uint256 resultLength = urlAndFilenameSafe ? (4 * data.length + 2) / 3 : 4 * ((data.length + 2) / 3);
71: 
72:         assembly ("memory-safe") {
73:             result := mload(0x40)
74: 
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Base64.sol:157`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
155:         }
156: 
157:         assembly ("memory-safe") {
158:             result := mload(0x40)
159: 
```

### [Informational] glamsterdam-block-context

- **Location**: `utils/Blockhash.sol:29`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
27:      */
28:     function blockHash(uint256 blockNumber) internal view returns (bytes32) {
29:         uint256 current = block.number;
30:         uint256 distance;
31: 
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Blockhash.sol:42`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
40:     /// @dev Internal function to query the EIP-2935 history storage contract.
41:     function _historyStorageCall(uint256 blockNumber) private view returns (bytes32 hash) {
42:         assembly ("memory-safe") {
43:             // Store the blockNumber in scratch space
44:             mstore(0x00, blockNumber)
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Bytes.sol:32`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
30:     function indexOf(bytes memory buffer, bytes1 s, uint256 pos) internal pure returns (uint256) {
31:         uint256 length = buffer.length;
32:         for (uint256 i = pos; i < length; ++i) {
33:             if (bytes1(_unsafeReadBytesOffset(buffer, i)) == s) {
34:                 return i;
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Bytes.sol:61`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
59:         unchecked {
60:             uint256 length = buffer.length;
61:             for (uint256 i = Math.min(Math.saturatingAdd(pos, 1), length); i > 0; --i) {
62:                 if (bytes1(_unsafeReadBytesOffset(buffer, i - 1)) == s) {
63:                     return i - 1;
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Bytes.sol:93`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
91:         // allocate and copy
92:         bytes memory result = new bytes(end - start);
93:         assembly ("memory-safe") {
94:             mcopy(add(result, 0x20), add(add(buffer, 0x20), start), sub(end, start))
95:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Bytes.sol:123`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
121: 
122:         // move and resize
123:         assembly ("memory-safe") {
124:             mcopy(add(buffer, 0x20), add(add(buffer, 0x20), start), sub(end, start))
125:             mstore(buffer, sub(end, start))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Bytes.sol:167`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
165: 
166:         // replace
167:         assembly ("memory-safe") {
168:             mcopy(add(add(buffer, 0x20), pos), add(add(replacement, 0x20), offset), length)
169:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Bytes.sol:180`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
178:      * `abi.encodePacked`.
179:      *
180:      * NOTE: this could be done in assembly with a single loop that expands starting at the FMP, but that would be
181:      * significantly less readable. It might be worth benchmarking the savings of the full-assembly approach.
182:      */
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Bytes.sol:181`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
179:      *
180:      * NOTE: this could be done in assembly with a single loop that expands starting at the FMP, but that would be
181:      * significantly less readable. It might be worth benchmarking the savings of the full-assembly approach.
182:      */
183:     function concat(bytes[] memory buffers) internal pure returns (bytes memory) {
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Bytes.sol:185`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
183:     function concat(bytes[] memory buffers) internal pure returns (bytes memory) {
184:         uint256 length = 0;
185:         for (uint256 i = 0; i < buffers.length; ++i) {
186:             length += buffers[i].length;
187:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Bytes.sol:192`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
190: 
191:         uint256 offset = 0x20;
192:         for (uint256 i = 0; i < buffers.length; ++i) {
193:             bytes memory input = buffers[i];
194:             assembly ("memory-safe") {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Bytes.sol:194`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
192:         for (uint256 i = 0; i < buffers.length; ++i) {
193:             bytes memory input = buffers[i];
194:             assembly ("memory-safe") {
195:                 mcopy(add(result, offset), add(input, 0x20), mload(input))
196:             }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Bytes.sol:211`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
209:      */
210:     function toNibbles(bytes memory input) internal pure returns (bytes memory output) {
211:         assembly ("memory-safe") {
212:             let length := mload(input)
213:             output := mload(0x40)
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Bytes.sol:311`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
309:      */
310:     function clz(bytes memory buffer) internal pure returns (uint256) {
311:         for (uint256 i = 0; i < buffer.length; i += 0x20) {
312:             bytes32 chunk = _unsafeReadBytesOffset(buffer, i);
313:             if (chunk != bytes32(0)) {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Bytes.sol:324`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
322:      *
323:      * NOTE: making this function internal would mean it could be used with memory unsafe offset, and marking the
324:      * assembly block as such would prevent some optimizations.
325:      */
326:     function _unsafeReadBytesOffset(bytes memory buffer, uint256 offset) private pure returns (bytes32 value) {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Bytes.sol:328`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
326:     function _unsafeReadBytesOffset(bytes memory buffer, uint256 offset) private pure returns (bytes32 value) {
327:         // This is not memory safe in the general case, but all calls to this private function are within bounds.
328:         assembly ("memory-safe") {
329:             value := mload(add(add(buffer, 0x20), offset))
330:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Calldata.sol:12`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
10:     // slither-disable-next-line write-after-write
11:     function emptyBytes() internal pure returns (bytes calldata result) {
12:         assembly ("memory-safe") {
13:             result.offset := 0
14:             result.length := 0
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Calldata.sol:20`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
18:     // slither-disable-next-line write-after-write
19:     function emptyString() internal pure returns (string calldata result) {
20:         assembly ("memory-safe") {
21:             result.offset := 0
22:             result.length := 0
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Create2.sol:45`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
43:             revert Create2EmptyBytecode();
44:         }
45:         assembly ("memory-safe") {
46:             addr := create2(amount, add(bytecode, 0x20), mload(bytecode), salt)
47:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Create2.sol:70`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
68:      */
69:     function computeAddress(bytes32 salt, bytes32 bytecodeHash, address deployer) internal pure returns (address addr) {
70:         assembly ("memory-safe") {
71:             let ptr := mload(0x40) // Get free memory pointer
72: 
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/LowLevelCall.sol:20`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
18:     /// @dev Same as {callNoReturn-address-bytes}, but allows specifying the value to be sent in the call.
19:     function callNoReturn(address target, uint256 value, bytes memory data) internal returns (bool success) {
20:         assembly ("memory-safe") {
21:             success := call(gas(), target, value, add(data, 0x20), mload(data), 0x00, 0x00)
22:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/LowLevelCall.sol:43`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
41:         bytes memory data
42:     ) internal returns (bool success, bytes32 result1, bytes32 result2) {
43:         assembly ("memory-safe") {
44:             success := call(gas(), target, value, add(data, 0x20), mload(data), 0x00, 0x40)
45:             result1 := mload(0x00)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/LowLevelCall.sol:52`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
50:     /// @dev Performs a Solidity function call using a low level `staticcall` and ignoring the return data.
51:     function staticcallNoReturn(address target, bytes memory data) internal view returns (bool success) {
52:         assembly ("memory-safe") {
53:             success := staticcall(gas(), target, add(data, 0x20), mload(data), 0x00, 0x00)
54:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/LowLevelCall.sol:66`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
64:         bytes memory data
65:     ) internal view returns (bool success, bytes32 result1, bytes32 result2) {
66:         assembly ("memory-safe") {
67:             success := staticcall(gas(), target, add(data, 0x20), mload(data), 0x00, 0x40)
68:             result1 := mload(0x00)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/LowLevelCall.sol:75`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
73:     /// @dev Performs a Solidity function call using a low level `delegatecall` and ignoring the return data.
74:     function delegatecallNoReturn(address target, bytes memory data) internal returns (bool success) {
75:         assembly ("memory-safe") {
76:             success := delegatecall(gas(), target, add(data, 0x20), mload(data), 0x00, 0x00)
77:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/LowLevelCall.sol:89`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
87:         bytes memory data
88:     ) internal returns (bool success, bytes32 result1, bytes32 result2) {
89:         assembly ("memory-safe") {
90:             success := delegatecall(gas(), target, add(data, 0x20), mload(data), 0x00, 0x40)
91:             result1 := mload(0x00)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/LowLevelCall.sol:98`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
96:     /// @dev Returns the size of the return data buffer.
97:     function returnDataSize() internal pure returns (uint256 size) {
98:         assembly ("memory-safe") {
99:             size := returndatasize()
100:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/LowLevelCall.sol:105`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
103:     /// @dev Returns a buffer containing the return data from the last call.
104:     function returnData() internal pure returns (bytes memory result) {
105:         assembly ("memory-safe") {
106:             result := mload(0x40)
107:             mstore(result, returndatasize())
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/LowLevelCall.sol:115`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
113:     /// @dev Revert with the return data from the last call.
114:     function bubbleRevert() internal pure {
115:         assembly ("memory-safe") {
116:             let fmp := mload(0x40)
117:             returndatacopy(fmp, 0x00, returndatasize())
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/LowLevelCall.sol:123`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
121: 
122:     function bubbleRevert(bytes memory returndata) internal pure {
123:         assembly ("memory-safe") {
124:             revert(add(returndata, 0x20), mload(returndata))
125:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Memory.sol:25`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
23:     /// @dev Returns a `Pointer` to the current free `Pointer`.
24:     function getFreeMemoryPointer() internal pure returns (Pointer ptr) {
25:         assembly ("memory-safe") {
26:             ptr := mload(0x40)
27:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Memory.sol:40`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
38:      **/
39:     function unsafeSetFreeMemoryPointer(Pointer ptr) internal pure {
40:         assembly ("memory-safe") {
41:             mstore(0x40, ptr)
42:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Memory.sol:59`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
57:     /// @dev Get a slice representation of a bytes object in memory
58:     function asSlice(bytes memory self) internal pure returns (Slice result) {
59:         assembly ("memory-safe") {
60:             result := or(shl(128, mload(self)), add(self, 0x20))
61:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Memory.sol:66`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
64:     /// @dev Returns the length of a given slice (equiv to self.length for calldata slices)
65:     function length(Slice self) internal pure returns (uint256 result) {
66:         assembly ("memory-safe") {
67:             result := shr(128, self)
68:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Memory.sol:92`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
90:         if (outOfBoundBytes > 0x1f) Panic.panic(Panic.ARRAY_OUT_OF_BOUNDS);
91: 
92:         assembly ("memory-safe") {
93:             value := and(mload(add(and(self, shr(128, not(0))), offset)), shl(mul(8, outOfBoundBytes), not(0)))
94:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Memory.sol:101`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
99:         uint256 len = length(self);
100:         Memory.Pointer ptr = _pointer(self);
101:         assembly ("memory-safe") {
102:             result := mload(0x40)
103:             mstore(result, len)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Memory.sol:115`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
113:         uint256 lenA = length(a);
114:         uint256 lenB = length(b);
115:         assembly ("memory-safe") {
116:             result := eq(keccak256(ptrA, lenA), keccak256(ptrB, lenB))
117:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Memory.sol:124`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
122:         Memory.Pointer fmp = getFreeMemoryPointer();
123:         Memory.Pointer end = forward(_pointer(self), length(self));
124:         assembly ("memory-safe") {
125:             result := iszero(lt(fmp, end)) // end <= fmp
126:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Memory.sol:138`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
136:      */
137:     function _asSlice(uint256 len, Memory.Pointer ptr) private pure returns (Slice result) {
138:         assembly ("memory-safe") {
139:             result := or(shl(128, len), ptr)
140:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Memory.sol:145`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
143:     /// @dev Returns the memory location of a given slice (equiv to self.offset for calldata slices)
144:     function _pointer(Slice self) private pure returns (Memory.Pointer result) {
145:         assembly ("memory-safe") {
146:             result := and(self, shr(128, not(0)))
147:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Multicall.sol:32`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
30: 
31:         results = new bytes[](data.length);
32:         for (uint256 i = 0; i < data.length; i++) {
33:             results[i] = Address.functionDelegateCall(address(this), bytes.concat(data[i], context));
34:         }
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `utils/Packing.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Rule confidence**: low
- **Rule rationale**: File size is a rough proxy for deployed bytecode size. A raised max contract size would relax rather than break constraints, so this is a watch point only.
- **Related fork candidates**: EIP-7907 (meter and increase contract code size, candidate)
- **Manual review required**: Yes

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:40`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
38: 
39:     function pack_1_1(bytes1 left, bytes1 right) internal pure returns (bytes2 result) {
40:         assembly ("memory-safe") {
41:             left := and(left, shl(248, not(0)))
42:             right := and(right, shl(248, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:48`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
46: 
47:     function pack_2_2(bytes2 left, bytes2 right) internal pure returns (bytes4 result) {
48:         assembly ("memory-safe") {
49:             left := and(left, shl(240, not(0)))
50:             right := and(right, shl(240, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:56`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
54: 
55:     function pack_2_4(bytes2 left, bytes4 right) internal pure returns (bytes6 result) {
56:         assembly ("memory-safe") {
57:             left := and(left, shl(240, not(0)))
58:             right := and(right, shl(224, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:64`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
62: 
63:     function pack_2_6(bytes2 left, bytes6 right) internal pure returns (bytes8 result) {
64:         assembly ("memory-safe") {
65:             left := and(left, shl(240, not(0)))
66:             right := and(right, shl(208, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:72`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
70: 
71:     function pack_2_8(bytes2 left, bytes8 right) internal pure returns (bytes10 result) {
72:         assembly ("memory-safe") {
73:             left := and(left, shl(240, not(0)))
74:             right := and(right, shl(192, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:80`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
78: 
79:     function pack_2_10(bytes2 left, bytes10 right) internal pure returns (bytes12 result) {
80:         assembly ("memory-safe") {
81:             left := and(left, shl(240, not(0)))
82:             right := and(right, shl(176, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:88`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
86: 
87:     function pack_2_20(bytes2 left, bytes20 right) internal pure returns (bytes22 result) {
88:         assembly ("memory-safe") {
89:             left := and(left, shl(240, not(0)))
90:             right := and(right, shl(96, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:96`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
94: 
95:     function pack_2_22(bytes2 left, bytes22 right) internal pure returns (bytes24 result) {
96:         assembly ("memory-safe") {
97:             left := and(left, shl(240, not(0)))
98:             right := and(right, shl(80, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:104`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
102: 
103:     function pack_4_2(bytes4 left, bytes2 right) internal pure returns (bytes6 result) {
104:         assembly ("memory-safe") {
105:             left := and(left, shl(224, not(0)))
106:             right := and(right, shl(240, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:112`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
110: 
111:     function pack_4_4(bytes4 left, bytes4 right) internal pure returns (bytes8 result) {
112:         assembly ("memory-safe") {
113:             left := and(left, shl(224, not(0)))
114:             right := and(right, shl(224, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:120`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
118: 
119:     function pack_4_6(bytes4 left, bytes6 right) internal pure returns (bytes10 result) {
120:         assembly ("memory-safe") {
121:             left := and(left, shl(224, not(0)))
122:             right := and(right, shl(208, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:128`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
126: 
127:     function pack_4_8(bytes4 left, bytes8 right) internal pure returns (bytes12 result) {
128:         assembly ("memory-safe") {
129:             left := and(left, shl(224, not(0)))
130:             right := and(right, shl(192, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:136`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
134: 
135:     function pack_4_12(bytes4 left, bytes12 right) internal pure returns (bytes16 result) {
136:         assembly ("memory-safe") {
137:             left := and(left, shl(224, not(0)))
138:             right := and(right, shl(160, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:144`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
142: 
143:     function pack_4_16(bytes4 left, bytes16 right) internal pure returns (bytes20 result) {
144:         assembly ("memory-safe") {
145:             left := and(left, shl(224, not(0)))
146:             right := and(right, shl(128, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:152`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
150: 
151:     function pack_4_20(bytes4 left, bytes20 right) internal pure returns (bytes24 result) {
152:         assembly ("memory-safe") {
153:             left := and(left, shl(224, not(0)))
154:             right := and(right, shl(96, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:160`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
158: 
159:     function pack_4_24(bytes4 left, bytes24 right) internal pure returns (bytes28 result) {
160:         assembly ("memory-safe") {
161:             left := and(left, shl(224, not(0)))
162:             right := and(right, shl(64, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:168`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
166: 
167:     function pack_4_28(bytes4 left, bytes28 right) internal pure returns (bytes32 result) {
168:         assembly ("memory-safe") {
169:             left := and(left, shl(224, not(0)))
170:             right := and(right, shl(32, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:176`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
174: 
175:     function pack_6_2(bytes6 left, bytes2 right) internal pure returns (bytes8 result) {
176:         assembly ("memory-safe") {
177:             left := and(left, shl(208, not(0)))
178:             right := and(right, shl(240, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:184`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
182: 
183:     function pack_6_4(bytes6 left, bytes4 right) internal pure returns (bytes10 result) {
184:         assembly ("memory-safe") {
185:             left := and(left, shl(208, not(0)))
186:             right := and(right, shl(224, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:192`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
190: 
191:     function pack_6_6(bytes6 left, bytes6 right) internal pure returns (bytes12 result) {
192:         assembly ("memory-safe") {
193:             left := and(left, shl(208, not(0)))
194:             right := and(right, shl(208, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:200`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
198: 
199:     function pack_6_10(bytes6 left, bytes10 right) internal pure returns (bytes16 result) {
200:         assembly ("memory-safe") {
201:             left := and(left, shl(208, not(0)))
202:             right := and(right, shl(176, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:208`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
206: 
207:     function pack_6_16(bytes6 left, bytes16 right) internal pure returns (bytes22 result) {
208:         assembly ("memory-safe") {
209:             left := and(left, shl(208, not(0)))
210:             right := and(right, shl(128, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:216`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
214: 
215:     function pack_6_22(bytes6 left, bytes22 right) internal pure returns (bytes28 result) {
216:         assembly ("memory-safe") {
217:             left := and(left, shl(208, not(0)))
218:             right := and(right, shl(80, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:224`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
222: 
223:     function pack_8_2(bytes8 left, bytes2 right) internal pure returns (bytes10 result) {
224:         assembly ("memory-safe") {
225:             left := and(left, shl(192, not(0)))
226:             right := and(right, shl(240, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:232`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
230: 
231:     function pack_8_4(bytes8 left, bytes4 right) internal pure returns (bytes12 result) {
232:         assembly ("memory-safe") {
233:             left := and(left, shl(192, not(0)))
234:             right := and(right, shl(224, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:240`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
238: 
239:     function pack_8_8(bytes8 left, bytes8 right) internal pure returns (bytes16 result) {
240:         assembly ("memory-safe") {
241:             left := and(left, shl(192, not(0)))
242:             right := and(right, shl(192, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:248`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
246: 
247:     function pack_8_12(bytes8 left, bytes12 right) internal pure returns (bytes20 result) {
248:         assembly ("memory-safe") {
249:             left := and(left, shl(192, not(0)))
250:             right := and(right, shl(160, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:256`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
254: 
255:     function pack_8_16(bytes8 left, bytes16 right) internal pure returns (bytes24 result) {
256:         assembly ("memory-safe") {
257:             left := and(left, shl(192, not(0)))
258:             right := and(right, shl(128, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:264`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
262: 
263:     function pack_8_20(bytes8 left, bytes20 right) internal pure returns (bytes28 result) {
264:         assembly ("memory-safe") {
265:             left := and(left, shl(192, not(0)))
266:             right := and(right, shl(96, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:272`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
270: 
271:     function pack_8_24(bytes8 left, bytes24 right) internal pure returns (bytes32 result) {
272:         assembly ("memory-safe") {
273:             left := and(left, shl(192, not(0)))
274:             right := and(right, shl(64, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:280`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
278: 
279:     function pack_10_2(bytes10 left, bytes2 right) internal pure returns (bytes12 result) {
280:         assembly ("memory-safe") {
281:             left := and(left, shl(176, not(0)))
282:             right := and(right, shl(240, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:288`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
286: 
287:     function pack_10_6(bytes10 left, bytes6 right) internal pure returns (bytes16 result) {
288:         assembly ("memory-safe") {
289:             left := and(left, shl(176, not(0)))
290:             right := and(right, shl(208, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:296`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
294: 
295:     function pack_10_10(bytes10 left, bytes10 right) internal pure returns (bytes20 result) {
296:         assembly ("memory-safe") {
297:             left := and(left, shl(176, not(0)))
298:             right := and(right, shl(176, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:304`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
302: 
303:     function pack_10_12(bytes10 left, bytes12 right) internal pure returns (bytes22 result) {
304:         assembly ("memory-safe") {
305:             left := and(left, shl(176, not(0)))
306:             right := and(right, shl(160, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:312`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
310: 
311:     function pack_10_22(bytes10 left, bytes22 right) internal pure returns (bytes32 result) {
312:         assembly ("memory-safe") {
313:             left := and(left, shl(176, not(0)))
314:             right := and(right, shl(80, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:320`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
318: 
319:     function pack_12_4(bytes12 left, bytes4 right) internal pure returns (bytes16 result) {
320:         assembly ("memory-safe") {
321:             left := and(left, shl(160, not(0)))
322:             right := and(right, shl(224, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:328`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
326: 
327:     function pack_12_8(bytes12 left, bytes8 right) internal pure returns (bytes20 result) {
328:         assembly ("memory-safe") {
329:             left := and(left, shl(160, not(0)))
330:             right := and(right, shl(192, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:336`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
334: 
335:     function pack_12_10(bytes12 left, bytes10 right) internal pure returns (bytes22 result) {
336:         assembly ("memory-safe") {
337:             left := and(left, shl(160, not(0)))
338:             right := and(right, shl(176, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:344`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
342: 
343:     function pack_12_12(bytes12 left, bytes12 right) internal pure returns (bytes24 result) {
344:         assembly ("memory-safe") {
345:             left := and(left, shl(160, not(0)))
346:             right := and(right, shl(160, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:352`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
350: 
351:     function pack_12_16(bytes12 left, bytes16 right) internal pure returns (bytes28 result) {
352:         assembly ("memory-safe") {
353:             left := and(left, shl(160, not(0)))
354:             right := and(right, shl(128, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:360`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
358: 
359:     function pack_12_20(bytes12 left, bytes20 right) internal pure returns (bytes32 result) {
360:         assembly ("memory-safe") {
361:             left := and(left, shl(160, not(0)))
362:             right := and(right, shl(96, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:368`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
366: 
367:     function pack_16_4(bytes16 left, bytes4 right) internal pure returns (bytes20 result) {
368:         assembly ("memory-safe") {
369:             left := and(left, shl(128, not(0)))
370:             right := and(right, shl(224, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:376`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
374: 
375:     function pack_16_6(bytes16 left, bytes6 right) internal pure returns (bytes22 result) {
376:         assembly ("memory-safe") {
377:             left := and(left, shl(128, not(0)))
378:             right := and(right, shl(208, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:384`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
382: 
383:     function pack_16_8(bytes16 left, bytes8 right) internal pure returns (bytes24 result) {
384:         assembly ("memory-safe") {
385:             left := and(left, shl(128, not(0)))
386:             right := and(right, shl(192, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:392`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
390: 
391:     function pack_16_12(bytes16 left, bytes12 right) internal pure returns (bytes28 result) {
392:         assembly ("memory-safe") {
393:             left := and(left, shl(128, not(0)))
394:             right := and(right, shl(160, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:400`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
398: 
399:     function pack_16_16(bytes16 left, bytes16 right) internal pure returns (bytes32 result) {
400:         assembly ("memory-safe") {
401:             left := and(left, shl(128, not(0)))
402:             right := and(right, shl(128, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:408`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
406: 
407:     function pack_20_2(bytes20 left, bytes2 right) internal pure returns (bytes22 result) {
408:         assembly ("memory-safe") {
409:             left := and(left, shl(96, not(0)))
410:             right := and(right, shl(240, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:416`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
414: 
415:     function pack_20_4(bytes20 left, bytes4 right) internal pure returns (bytes24 result) {
416:         assembly ("memory-safe") {
417:             left := and(left, shl(96, not(0)))
418:             right := and(right, shl(224, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:424`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
422: 
423:     function pack_20_8(bytes20 left, bytes8 right) internal pure returns (bytes28 result) {
424:         assembly ("memory-safe") {
425:             left := and(left, shl(96, not(0)))
426:             right := and(right, shl(192, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:432`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
430: 
431:     function pack_20_12(bytes20 left, bytes12 right) internal pure returns (bytes32 result) {
432:         assembly ("memory-safe") {
433:             left := and(left, shl(96, not(0)))
434:             right := and(right, shl(160, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:440`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
438: 
439:     function pack_22_2(bytes22 left, bytes2 right) internal pure returns (bytes24 result) {
440:         assembly ("memory-safe") {
441:             left := and(left, shl(80, not(0)))
442:             right := and(right, shl(240, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:448`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
446: 
447:     function pack_22_6(bytes22 left, bytes6 right) internal pure returns (bytes28 result) {
448:         assembly ("memory-safe") {
449:             left := and(left, shl(80, not(0)))
450:             right := and(right, shl(208, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:456`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
454: 
455:     function pack_22_10(bytes22 left, bytes10 right) internal pure returns (bytes32 result) {
456:         assembly ("memory-safe") {
457:             left := and(left, shl(80, not(0)))
458:             right := and(right, shl(176, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:464`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
462: 
463:     function pack_24_4(bytes24 left, bytes4 right) internal pure returns (bytes28 result) {
464:         assembly ("memory-safe") {
465:             left := and(left, shl(64, not(0)))
466:             right := and(right, shl(224, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:472`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
470: 
471:     function pack_24_8(bytes24 left, bytes8 right) internal pure returns (bytes32 result) {
472:         assembly ("memory-safe") {
473:             left := and(left, shl(64, not(0)))
474:             right := and(right, shl(192, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:480`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
478: 
479:     function pack_28_4(bytes28 left, bytes4 right) internal pure returns (bytes32 result) {
480:         assembly ("memory-safe") {
481:             left := and(left, shl(32, not(0)))
482:             right := and(right, shl(224, not(0)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:489`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
487:     function extract_2_1(bytes2 self, uint8 offset) internal pure returns (bytes1 result) {
488:         if (offset > 1) revert OutOfRangeAccess();
489:         assembly ("memory-safe") {
490:             result := and(shl(mul(8, offset), self), shl(248, not(0)))
491:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:496`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
494:     function replace_2_1(bytes2 self, bytes1 value, uint8 offset) internal pure returns (bytes2 result) {
495:         bytes1 oldValue = extract_2_1(self, offset);
496:         assembly ("memory-safe") {
497:             value := and(value, shl(248, not(0)))
498:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:504`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
502:     function extract_4_1(bytes4 self, uint8 offset) internal pure returns (bytes1 result) {
503:         if (offset > 3) revert OutOfRangeAccess();
504:         assembly ("memory-safe") {
505:             result := and(shl(mul(8, offset), self), shl(248, not(0)))
506:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:511`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
509:     function replace_4_1(bytes4 self, bytes1 value, uint8 offset) internal pure returns (bytes4 result) {
510:         bytes1 oldValue = extract_4_1(self, offset);
511:         assembly ("memory-safe") {
512:             value := and(value, shl(248, not(0)))
513:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:519`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
517:     function extract_4_2(bytes4 self, uint8 offset) internal pure returns (bytes2 result) {
518:         if (offset > 2) revert OutOfRangeAccess();
519:         assembly ("memory-safe") {
520:             result := and(shl(mul(8, offset), self), shl(240, not(0)))
521:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:526`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
524:     function replace_4_2(bytes4 self, bytes2 value, uint8 offset) internal pure returns (bytes4 result) {
525:         bytes2 oldValue = extract_4_2(self, offset);
526:         assembly ("memory-safe") {
527:             value := and(value, shl(240, not(0)))
528:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:534`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
532:     function extract_6_1(bytes6 self, uint8 offset) internal pure returns (bytes1 result) {
533:         if (offset > 5) revert OutOfRangeAccess();
534:         assembly ("memory-safe") {
535:             result := and(shl(mul(8, offset), self), shl(248, not(0)))
536:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:541`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
539:     function replace_6_1(bytes6 self, bytes1 value, uint8 offset) internal pure returns (bytes6 result) {
540:         bytes1 oldValue = extract_6_1(self, offset);
541:         assembly ("memory-safe") {
542:             value := and(value, shl(248, not(0)))
543:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:549`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
547:     function extract_6_2(bytes6 self, uint8 offset) internal pure returns (bytes2 result) {
548:         if (offset > 4) revert OutOfRangeAccess();
549:         assembly ("memory-safe") {
550:             result := and(shl(mul(8, offset), self), shl(240, not(0)))
551:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:556`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
554:     function replace_6_2(bytes6 self, bytes2 value, uint8 offset) internal pure returns (bytes6 result) {
555:         bytes2 oldValue = extract_6_2(self, offset);
556:         assembly ("memory-safe") {
557:             value := and(value, shl(240, not(0)))
558:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:564`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
562:     function extract_6_4(bytes6 self, uint8 offset) internal pure returns (bytes4 result) {
563:         if (offset > 2) revert OutOfRangeAccess();
564:         assembly ("memory-safe") {
565:             result := and(shl(mul(8, offset), self), shl(224, not(0)))
566:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:571`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
569:     function replace_6_4(bytes6 self, bytes4 value, uint8 offset) internal pure returns (bytes6 result) {
570:         bytes4 oldValue = extract_6_4(self, offset);
571:         assembly ("memory-safe") {
572:             value := and(value, shl(224, not(0)))
573:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:579`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
577:     function extract_8_1(bytes8 self, uint8 offset) internal pure returns (bytes1 result) {
578:         if (offset > 7) revert OutOfRangeAccess();
579:         assembly ("memory-safe") {
580:             result := and(shl(mul(8, offset), self), shl(248, not(0)))
581:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:586`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
584:     function replace_8_1(bytes8 self, bytes1 value, uint8 offset) internal pure returns (bytes8 result) {
585:         bytes1 oldValue = extract_8_1(self, offset);
586:         assembly ("memory-safe") {
587:             value := and(value, shl(248, not(0)))
588:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:594`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
592:     function extract_8_2(bytes8 self, uint8 offset) internal pure returns (bytes2 result) {
593:         if (offset > 6) revert OutOfRangeAccess();
594:         assembly ("memory-safe") {
595:             result := and(shl(mul(8, offset), self), shl(240, not(0)))
596:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:601`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
599:     function replace_8_2(bytes8 self, bytes2 value, uint8 offset) internal pure returns (bytes8 result) {
600:         bytes2 oldValue = extract_8_2(self, offset);
601:         assembly ("memory-safe") {
602:             value := and(value, shl(240, not(0)))
603:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:609`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
607:     function extract_8_4(bytes8 self, uint8 offset) internal pure returns (bytes4 result) {
608:         if (offset > 4) revert OutOfRangeAccess();
609:         assembly ("memory-safe") {
610:             result := and(shl(mul(8, offset), self), shl(224, not(0)))
611:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:616`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
614:     function replace_8_4(bytes8 self, bytes4 value, uint8 offset) internal pure returns (bytes8 result) {
615:         bytes4 oldValue = extract_8_4(self, offset);
616:         assembly ("memory-safe") {
617:             value := and(value, shl(224, not(0)))
618:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:624`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
622:     function extract_8_6(bytes8 self, uint8 offset) internal pure returns (bytes6 result) {
623:         if (offset > 2) revert OutOfRangeAccess();
624:         assembly ("memory-safe") {
625:             result := and(shl(mul(8, offset), self), shl(208, not(0)))
626:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:631`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
629:     function replace_8_6(bytes8 self, bytes6 value, uint8 offset) internal pure returns (bytes8 result) {
630:         bytes6 oldValue = extract_8_6(self, offset);
631:         assembly ("memory-safe") {
632:             value := and(value, shl(208, not(0)))
633:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:639`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
637:     function extract_10_1(bytes10 self, uint8 offset) internal pure returns (bytes1 result) {
638:         if (offset > 9) revert OutOfRangeAccess();
639:         assembly ("memory-safe") {
640:             result := and(shl(mul(8, offset), self), shl(248, not(0)))
641:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:646`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
644:     function replace_10_1(bytes10 self, bytes1 value, uint8 offset) internal pure returns (bytes10 result) {
645:         bytes1 oldValue = extract_10_1(self, offset);
646:         assembly ("memory-safe") {
647:             value := and(value, shl(248, not(0)))
648:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:654`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
652:     function extract_10_2(bytes10 self, uint8 offset) internal pure returns (bytes2 result) {
653:         if (offset > 8) revert OutOfRangeAccess();
654:         assembly ("memory-safe") {
655:             result := and(shl(mul(8, offset), self), shl(240, not(0)))
656:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:661`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
659:     function replace_10_2(bytes10 self, bytes2 value, uint8 offset) internal pure returns (bytes10 result) {
660:         bytes2 oldValue = extract_10_2(self, offset);
661:         assembly ("memory-safe") {
662:             value := and(value, shl(240, not(0)))
663:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:669`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
667:     function extract_10_4(bytes10 self, uint8 offset) internal pure returns (bytes4 result) {
668:         if (offset > 6) revert OutOfRangeAccess();
669:         assembly ("memory-safe") {
670:             result := and(shl(mul(8, offset), self), shl(224, not(0)))
671:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:676`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
674:     function replace_10_4(bytes10 self, bytes4 value, uint8 offset) internal pure returns (bytes10 result) {
675:         bytes4 oldValue = extract_10_4(self, offset);
676:         assembly ("memory-safe") {
677:             value := and(value, shl(224, not(0)))
678:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:684`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
682:     function extract_10_6(bytes10 self, uint8 offset) internal pure returns (bytes6 result) {
683:         if (offset > 4) revert OutOfRangeAccess();
684:         assembly ("memory-safe") {
685:             result := and(shl(mul(8, offset), self), shl(208, not(0)))
686:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:691`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
689:     function replace_10_6(bytes10 self, bytes6 value, uint8 offset) internal pure returns (bytes10 result) {
690:         bytes6 oldValue = extract_10_6(self, offset);
691:         assembly ("memory-safe") {
692:             value := and(value, shl(208, not(0)))
693:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:699`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
697:     function extract_10_8(bytes10 self, uint8 offset) internal pure returns (bytes8 result) {
698:         if (offset > 2) revert OutOfRangeAccess();
699:         assembly ("memory-safe") {
700:             result := and(shl(mul(8, offset), self), shl(192, not(0)))
701:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:706`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
704:     function replace_10_8(bytes10 self, bytes8 value, uint8 offset) internal pure returns (bytes10 result) {
705:         bytes8 oldValue = extract_10_8(self, offset);
706:         assembly ("memory-safe") {
707:             value := and(value, shl(192, not(0)))
708:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:714`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
712:     function extract_12_1(bytes12 self, uint8 offset) internal pure returns (bytes1 result) {
713:         if (offset > 11) revert OutOfRangeAccess();
714:         assembly ("memory-safe") {
715:             result := and(shl(mul(8, offset), self), shl(248, not(0)))
716:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:721`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
719:     function replace_12_1(bytes12 self, bytes1 value, uint8 offset) internal pure returns (bytes12 result) {
720:         bytes1 oldValue = extract_12_1(self, offset);
721:         assembly ("memory-safe") {
722:             value := and(value, shl(248, not(0)))
723:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:729`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
727:     function extract_12_2(bytes12 self, uint8 offset) internal pure returns (bytes2 result) {
728:         if (offset > 10) revert OutOfRangeAccess();
729:         assembly ("memory-safe") {
730:             result := and(shl(mul(8, offset), self), shl(240, not(0)))
731:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:736`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
734:     function replace_12_2(bytes12 self, bytes2 value, uint8 offset) internal pure returns (bytes12 result) {
735:         bytes2 oldValue = extract_12_2(self, offset);
736:         assembly ("memory-safe") {
737:             value := and(value, shl(240, not(0)))
738:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:744`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
742:     function extract_12_4(bytes12 self, uint8 offset) internal pure returns (bytes4 result) {
743:         if (offset > 8) revert OutOfRangeAccess();
744:         assembly ("memory-safe") {
745:             result := and(shl(mul(8, offset), self), shl(224, not(0)))
746:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:751`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
749:     function replace_12_4(bytes12 self, bytes4 value, uint8 offset) internal pure returns (bytes12 result) {
750:         bytes4 oldValue = extract_12_4(self, offset);
751:         assembly ("memory-safe") {
752:             value := and(value, shl(224, not(0)))
753:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:759`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
757:     function extract_12_6(bytes12 self, uint8 offset) internal pure returns (bytes6 result) {
758:         if (offset > 6) revert OutOfRangeAccess();
759:         assembly ("memory-safe") {
760:             result := and(shl(mul(8, offset), self), shl(208, not(0)))
761:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:766`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
764:     function replace_12_6(bytes12 self, bytes6 value, uint8 offset) internal pure returns (bytes12 result) {
765:         bytes6 oldValue = extract_12_6(self, offset);
766:         assembly ("memory-safe") {
767:             value := and(value, shl(208, not(0)))
768:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:774`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
772:     function extract_12_8(bytes12 self, uint8 offset) internal pure returns (bytes8 result) {
773:         if (offset > 4) revert OutOfRangeAccess();
774:         assembly ("memory-safe") {
775:             result := and(shl(mul(8, offset), self), shl(192, not(0)))
776:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:781`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
779:     function replace_12_8(bytes12 self, bytes8 value, uint8 offset) internal pure returns (bytes12 result) {
780:         bytes8 oldValue = extract_12_8(self, offset);
781:         assembly ("memory-safe") {
782:             value := and(value, shl(192, not(0)))
783:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:789`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
787:     function extract_12_10(bytes12 self, uint8 offset) internal pure returns (bytes10 result) {
788:         if (offset > 2) revert OutOfRangeAccess();
789:         assembly ("memory-safe") {
790:             result := and(shl(mul(8, offset), self), shl(176, not(0)))
791:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:796`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
794:     function replace_12_10(bytes12 self, bytes10 value, uint8 offset) internal pure returns (bytes12 result) {
795:         bytes10 oldValue = extract_12_10(self, offset);
796:         assembly ("memory-safe") {
797:             value := and(value, shl(176, not(0)))
798:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:804`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
802:     function extract_16_1(bytes16 self, uint8 offset) internal pure returns (bytes1 result) {
803:         if (offset > 15) revert OutOfRangeAccess();
804:         assembly ("memory-safe") {
805:             result := and(shl(mul(8, offset), self), shl(248, not(0)))
806:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:811`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
809:     function replace_16_1(bytes16 self, bytes1 value, uint8 offset) internal pure returns (bytes16 result) {
810:         bytes1 oldValue = extract_16_1(self, offset);
811:         assembly ("memory-safe") {
812:             value := and(value, shl(248, not(0)))
813:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:819`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
817:     function extract_16_2(bytes16 self, uint8 offset) internal pure returns (bytes2 result) {
818:         if (offset > 14) revert OutOfRangeAccess();
819:         assembly ("memory-safe") {
820:             result := and(shl(mul(8, offset), self), shl(240, not(0)))
821:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:826`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
824:     function replace_16_2(bytes16 self, bytes2 value, uint8 offset) internal pure returns (bytes16 result) {
825:         bytes2 oldValue = extract_16_2(self, offset);
826:         assembly ("memory-safe") {
827:             value := and(value, shl(240, not(0)))
828:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:834`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
832:     function extract_16_4(bytes16 self, uint8 offset) internal pure returns (bytes4 result) {
833:         if (offset > 12) revert OutOfRangeAccess();
834:         assembly ("memory-safe") {
835:             result := and(shl(mul(8, offset), self), shl(224, not(0)))
836:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:841`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
839:     function replace_16_4(bytes16 self, bytes4 value, uint8 offset) internal pure returns (bytes16 result) {
840:         bytes4 oldValue = extract_16_4(self, offset);
841:         assembly ("memory-safe") {
842:             value := and(value, shl(224, not(0)))
843:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:849`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
847:     function extract_16_6(bytes16 self, uint8 offset) internal pure returns (bytes6 result) {
848:         if (offset > 10) revert OutOfRangeAccess();
849:         assembly ("memory-safe") {
850:             result := and(shl(mul(8, offset), self), shl(208, not(0)))
851:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:856`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
854:     function replace_16_6(bytes16 self, bytes6 value, uint8 offset) internal pure returns (bytes16 result) {
855:         bytes6 oldValue = extract_16_6(self, offset);
856:         assembly ("memory-safe") {
857:             value := and(value, shl(208, not(0)))
858:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:864`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
862:     function extract_16_8(bytes16 self, uint8 offset) internal pure returns (bytes8 result) {
863:         if (offset > 8) revert OutOfRangeAccess();
864:         assembly ("memory-safe") {
865:             result := and(shl(mul(8, offset), self), shl(192, not(0)))
866:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:871`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
869:     function replace_16_8(bytes16 self, bytes8 value, uint8 offset) internal pure returns (bytes16 result) {
870:         bytes8 oldValue = extract_16_8(self, offset);
871:         assembly ("memory-safe") {
872:             value := and(value, shl(192, not(0)))
873:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:879`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
877:     function extract_16_10(bytes16 self, uint8 offset) internal pure returns (bytes10 result) {
878:         if (offset > 6) revert OutOfRangeAccess();
879:         assembly ("memory-safe") {
880:             result := and(shl(mul(8, offset), self), shl(176, not(0)))
881:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:886`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
884:     function replace_16_10(bytes16 self, bytes10 value, uint8 offset) internal pure returns (bytes16 result) {
885:         bytes10 oldValue = extract_16_10(self, offset);
886:         assembly ("memory-safe") {
887:             value := and(value, shl(176, not(0)))
888:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:894`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
892:     function extract_16_12(bytes16 self, uint8 offset) internal pure returns (bytes12 result) {
893:         if (offset > 4) revert OutOfRangeAccess();
894:         assembly ("memory-safe") {
895:             result := and(shl(mul(8, offset), self), shl(160, not(0)))
896:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:901`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
899:     function replace_16_12(bytes16 self, bytes12 value, uint8 offset) internal pure returns (bytes16 result) {
900:         bytes12 oldValue = extract_16_12(self, offset);
901:         assembly ("memory-safe") {
902:             value := and(value, shl(160, not(0)))
903:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:909`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
907:     function extract_20_1(bytes20 self, uint8 offset) internal pure returns (bytes1 result) {
908:         if (offset > 19) revert OutOfRangeAccess();
909:         assembly ("memory-safe") {
910:             result := and(shl(mul(8, offset), self), shl(248, not(0)))
911:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:916`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
914:     function replace_20_1(bytes20 self, bytes1 value, uint8 offset) internal pure returns (bytes20 result) {
915:         bytes1 oldValue = extract_20_1(self, offset);
916:         assembly ("memory-safe") {
917:             value := and(value, shl(248, not(0)))
918:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:924`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
922:     function extract_20_2(bytes20 self, uint8 offset) internal pure returns (bytes2 result) {
923:         if (offset > 18) revert OutOfRangeAccess();
924:         assembly ("memory-safe") {
925:             result := and(shl(mul(8, offset), self), shl(240, not(0)))
926:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:931`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
929:     function replace_20_2(bytes20 self, bytes2 value, uint8 offset) internal pure returns (bytes20 result) {
930:         bytes2 oldValue = extract_20_2(self, offset);
931:         assembly ("memory-safe") {
932:             value := and(value, shl(240, not(0)))
933:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:939`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
937:     function extract_20_4(bytes20 self, uint8 offset) internal pure returns (bytes4 result) {
938:         if (offset > 16) revert OutOfRangeAccess();
939:         assembly ("memory-safe") {
940:             result := and(shl(mul(8, offset), self), shl(224, not(0)))
941:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:946`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
944:     function replace_20_4(bytes20 self, bytes4 value, uint8 offset) internal pure returns (bytes20 result) {
945:         bytes4 oldValue = extract_20_4(self, offset);
946:         assembly ("memory-safe") {
947:             value := and(value, shl(224, not(0)))
948:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:954`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
952:     function extract_20_6(bytes20 self, uint8 offset) internal pure returns (bytes6 result) {
953:         if (offset > 14) revert OutOfRangeAccess();
954:         assembly ("memory-safe") {
955:             result := and(shl(mul(8, offset), self), shl(208, not(0)))
956:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:961`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
959:     function replace_20_6(bytes20 self, bytes6 value, uint8 offset) internal pure returns (bytes20 result) {
960:         bytes6 oldValue = extract_20_6(self, offset);
961:         assembly ("memory-safe") {
962:             value := and(value, shl(208, not(0)))
963:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:969`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
967:     function extract_20_8(bytes20 self, uint8 offset) internal pure returns (bytes8 result) {
968:         if (offset > 12) revert OutOfRangeAccess();
969:         assembly ("memory-safe") {
970:             result := and(shl(mul(8, offset), self), shl(192, not(0)))
971:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:976`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
974:     function replace_20_8(bytes20 self, bytes8 value, uint8 offset) internal pure returns (bytes20 result) {
975:         bytes8 oldValue = extract_20_8(self, offset);
976:         assembly ("memory-safe") {
977:             value := and(value, shl(192, not(0)))
978:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:984`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
982:     function extract_20_10(bytes20 self, uint8 offset) internal pure returns (bytes10 result) {
983:         if (offset > 10) revert OutOfRangeAccess();
984:         assembly ("memory-safe") {
985:             result := and(shl(mul(8, offset), self), shl(176, not(0)))
986:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:991`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
989:     function replace_20_10(bytes20 self, bytes10 value, uint8 offset) internal pure returns (bytes20 result) {
990:         bytes10 oldValue = extract_20_10(self, offset);
991:         assembly ("memory-safe") {
992:             value := and(value, shl(176, not(0)))
993:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:999`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
997:     function extract_20_12(bytes20 self, uint8 offset) internal pure returns (bytes12 result) {
998:         if (offset > 8) revert OutOfRangeAccess();
999:         assembly ("memory-safe") {
1000:             result := and(shl(mul(8, offset), self), shl(160, not(0)))
1001:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1006`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1004:     function replace_20_12(bytes20 self, bytes12 value, uint8 offset) internal pure returns (bytes20 result) {
1005:         bytes12 oldValue = extract_20_12(self, offset);
1006:         assembly ("memory-safe") {
1007:             value := and(value, shl(160, not(0)))
1008:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1014`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1012:     function extract_20_16(bytes20 self, uint8 offset) internal pure returns (bytes16 result) {
1013:         if (offset > 4) revert OutOfRangeAccess();
1014:         assembly ("memory-safe") {
1015:             result := and(shl(mul(8, offset), self), shl(128, not(0)))
1016:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1021`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1019:     function replace_20_16(bytes20 self, bytes16 value, uint8 offset) internal pure returns (bytes20 result) {
1020:         bytes16 oldValue = extract_20_16(self, offset);
1021:         assembly ("memory-safe") {
1022:             value := and(value, shl(128, not(0)))
1023:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1029`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1027:     function extract_22_1(bytes22 self, uint8 offset) internal pure returns (bytes1 result) {
1028:         if (offset > 21) revert OutOfRangeAccess();
1029:         assembly ("memory-safe") {
1030:             result := and(shl(mul(8, offset), self), shl(248, not(0)))
1031:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1036`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1034:     function replace_22_1(bytes22 self, bytes1 value, uint8 offset) internal pure returns (bytes22 result) {
1035:         bytes1 oldValue = extract_22_1(self, offset);
1036:         assembly ("memory-safe") {
1037:             value := and(value, shl(248, not(0)))
1038:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1044`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1042:     function extract_22_2(bytes22 self, uint8 offset) internal pure returns (bytes2 result) {
1043:         if (offset > 20) revert OutOfRangeAccess();
1044:         assembly ("memory-safe") {
1045:             result := and(shl(mul(8, offset), self), shl(240, not(0)))
1046:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1051`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1049:     function replace_22_2(bytes22 self, bytes2 value, uint8 offset) internal pure returns (bytes22 result) {
1050:         bytes2 oldValue = extract_22_2(self, offset);
1051:         assembly ("memory-safe") {
1052:             value := and(value, shl(240, not(0)))
1053:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1059`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1057:     function extract_22_4(bytes22 self, uint8 offset) internal pure returns (bytes4 result) {
1058:         if (offset > 18) revert OutOfRangeAccess();
1059:         assembly ("memory-safe") {
1060:             result := and(shl(mul(8, offset), self), shl(224, not(0)))
1061:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1066`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1064:     function replace_22_4(bytes22 self, bytes4 value, uint8 offset) internal pure returns (bytes22 result) {
1065:         bytes4 oldValue = extract_22_4(self, offset);
1066:         assembly ("memory-safe") {
1067:             value := and(value, shl(224, not(0)))
1068:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1074`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1072:     function extract_22_6(bytes22 self, uint8 offset) internal pure returns (bytes6 result) {
1073:         if (offset > 16) revert OutOfRangeAccess();
1074:         assembly ("memory-safe") {
1075:             result := and(shl(mul(8, offset), self), shl(208, not(0)))
1076:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1081`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1079:     function replace_22_6(bytes22 self, bytes6 value, uint8 offset) internal pure returns (bytes22 result) {
1080:         bytes6 oldValue = extract_22_6(self, offset);
1081:         assembly ("memory-safe") {
1082:             value := and(value, shl(208, not(0)))
1083:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1089`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1087:     function extract_22_8(bytes22 self, uint8 offset) internal pure returns (bytes8 result) {
1088:         if (offset > 14) revert OutOfRangeAccess();
1089:         assembly ("memory-safe") {
1090:             result := and(shl(mul(8, offset), self), shl(192, not(0)))
1091:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1096`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1094:     function replace_22_8(bytes22 self, bytes8 value, uint8 offset) internal pure returns (bytes22 result) {
1095:         bytes8 oldValue = extract_22_8(self, offset);
1096:         assembly ("memory-safe") {
1097:             value := and(value, shl(192, not(0)))
1098:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1104`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1102:     function extract_22_10(bytes22 self, uint8 offset) internal pure returns (bytes10 result) {
1103:         if (offset > 12) revert OutOfRangeAccess();
1104:         assembly ("memory-safe") {
1105:             result := and(shl(mul(8, offset), self), shl(176, not(0)))
1106:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1111`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1109:     function replace_22_10(bytes22 self, bytes10 value, uint8 offset) internal pure returns (bytes22 result) {
1110:         bytes10 oldValue = extract_22_10(self, offset);
1111:         assembly ("memory-safe") {
1112:             value := and(value, shl(176, not(0)))
1113:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1119`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1117:     function extract_22_12(bytes22 self, uint8 offset) internal pure returns (bytes12 result) {
1118:         if (offset > 10) revert OutOfRangeAccess();
1119:         assembly ("memory-safe") {
1120:             result := and(shl(mul(8, offset), self), shl(160, not(0)))
1121:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1126`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1124:     function replace_22_12(bytes22 self, bytes12 value, uint8 offset) internal pure returns (bytes22 result) {
1125:         bytes12 oldValue = extract_22_12(self, offset);
1126:         assembly ("memory-safe") {
1127:             value := and(value, shl(160, not(0)))
1128:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1134`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1132:     function extract_22_16(bytes22 self, uint8 offset) internal pure returns (bytes16 result) {
1133:         if (offset > 6) revert OutOfRangeAccess();
1134:         assembly ("memory-safe") {
1135:             result := and(shl(mul(8, offset), self), shl(128, not(0)))
1136:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1141`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1139:     function replace_22_16(bytes22 self, bytes16 value, uint8 offset) internal pure returns (bytes22 result) {
1140:         bytes16 oldValue = extract_22_16(self, offset);
1141:         assembly ("memory-safe") {
1142:             value := and(value, shl(128, not(0)))
1143:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1149`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1147:     function extract_22_20(bytes22 self, uint8 offset) internal pure returns (bytes20 result) {
1148:         if (offset > 2) revert OutOfRangeAccess();
1149:         assembly ("memory-safe") {
1150:             result := and(shl(mul(8, offset), self), shl(96, not(0)))
1151:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1156`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1154:     function replace_22_20(bytes22 self, bytes20 value, uint8 offset) internal pure returns (bytes22 result) {
1155:         bytes20 oldValue = extract_22_20(self, offset);
1156:         assembly ("memory-safe") {
1157:             value := and(value, shl(96, not(0)))
1158:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1164`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1162:     function extract_24_1(bytes24 self, uint8 offset) internal pure returns (bytes1 result) {
1163:         if (offset > 23) revert OutOfRangeAccess();
1164:         assembly ("memory-safe") {
1165:             result := and(shl(mul(8, offset), self), shl(248, not(0)))
1166:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1171`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1169:     function replace_24_1(bytes24 self, bytes1 value, uint8 offset) internal pure returns (bytes24 result) {
1170:         bytes1 oldValue = extract_24_1(self, offset);
1171:         assembly ("memory-safe") {
1172:             value := and(value, shl(248, not(0)))
1173:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1179`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1177:     function extract_24_2(bytes24 self, uint8 offset) internal pure returns (bytes2 result) {
1178:         if (offset > 22) revert OutOfRangeAccess();
1179:         assembly ("memory-safe") {
1180:             result := and(shl(mul(8, offset), self), shl(240, not(0)))
1181:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1186`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1184:     function replace_24_2(bytes24 self, bytes2 value, uint8 offset) internal pure returns (bytes24 result) {
1185:         bytes2 oldValue = extract_24_2(self, offset);
1186:         assembly ("memory-safe") {
1187:             value := and(value, shl(240, not(0)))
1188:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1194`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1192:     function extract_24_4(bytes24 self, uint8 offset) internal pure returns (bytes4 result) {
1193:         if (offset > 20) revert OutOfRangeAccess();
1194:         assembly ("memory-safe") {
1195:             result := and(shl(mul(8, offset), self), shl(224, not(0)))
1196:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1201`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1199:     function replace_24_4(bytes24 self, bytes4 value, uint8 offset) internal pure returns (bytes24 result) {
1200:         bytes4 oldValue = extract_24_4(self, offset);
1201:         assembly ("memory-safe") {
1202:             value := and(value, shl(224, not(0)))
1203:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1209`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1207:     function extract_24_6(bytes24 self, uint8 offset) internal pure returns (bytes6 result) {
1208:         if (offset > 18) revert OutOfRangeAccess();
1209:         assembly ("memory-safe") {
1210:             result := and(shl(mul(8, offset), self), shl(208, not(0)))
1211:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1216`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1214:     function replace_24_6(bytes24 self, bytes6 value, uint8 offset) internal pure returns (bytes24 result) {
1215:         bytes6 oldValue = extract_24_6(self, offset);
1216:         assembly ("memory-safe") {
1217:             value := and(value, shl(208, not(0)))
1218:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1224`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1222:     function extract_24_8(bytes24 self, uint8 offset) internal pure returns (bytes8 result) {
1223:         if (offset > 16) revert OutOfRangeAccess();
1224:         assembly ("memory-safe") {
1225:             result := and(shl(mul(8, offset), self), shl(192, not(0)))
1226:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1231`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1229:     function replace_24_8(bytes24 self, bytes8 value, uint8 offset) internal pure returns (bytes24 result) {
1230:         bytes8 oldValue = extract_24_8(self, offset);
1231:         assembly ("memory-safe") {
1232:             value := and(value, shl(192, not(0)))
1233:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1239`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1237:     function extract_24_10(bytes24 self, uint8 offset) internal pure returns (bytes10 result) {
1238:         if (offset > 14) revert OutOfRangeAccess();
1239:         assembly ("memory-safe") {
1240:             result := and(shl(mul(8, offset), self), shl(176, not(0)))
1241:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1246`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1244:     function replace_24_10(bytes24 self, bytes10 value, uint8 offset) internal pure returns (bytes24 result) {
1245:         bytes10 oldValue = extract_24_10(self, offset);
1246:         assembly ("memory-safe") {
1247:             value := and(value, shl(176, not(0)))
1248:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1254`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1252:     function extract_24_12(bytes24 self, uint8 offset) internal pure returns (bytes12 result) {
1253:         if (offset > 12) revert OutOfRangeAccess();
1254:         assembly ("memory-safe") {
1255:             result := and(shl(mul(8, offset), self), shl(160, not(0)))
1256:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1261`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1259:     function replace_24_12(bytes24 self, bytes12 value, uint8 offset) internal pure returns (bytes24 result) {
1260:         bytes12 oldValue = extract_24_12(self, offset);
1261:         assembly ("memory-safe") {
1262:             value := and(value, shl(160, not(0)))
1263:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1269`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1267:     function extract_24_16(bytes24 self, uint8 offset) internal pure returns (bytes16 result) {
1268:         if (offset > 8) revert OutOfRangeAccess();
1269:         assembly ("memory-safe") {
1270:             result := and(shl(mul(8, offset), self), shl(128, not(0)))
1271:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1276`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1274:     function replace_24_16(bytes24 self, bytes16 value, uint8 offset) internal pure returns (bytes24 result) {
1275:         bytes16 oldValue = extract_24_16(self, offset);
1276:         assembly ("memory-safe") {
1277:             value := and(value, shl(128, not(0)))
1278:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1284`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1282:     function extract_24_20(bytes24 self, uint8 offset) internal pure returns (bytes20 result) {
1283:         if (offset > 4) revert OutOfRangeAccess();
1284:         assembly ("memory-safe") {
1285:             result := and(shl(mul(8, offset), self), shl(96, not(0)))
1286:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1291`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1289:     function replace_24_20(bytes24 self, bytes20 value, uint8 offset) internal pure returns (bytes24 result) {
1290:         bytes20 oldValue = extract_24_20(self, offset);
1291:         assembly ("memory-safe") {
1292:             value := and(value, shl(96, not(0)))
1293:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1299`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1297:     function extract_24_22(bytes24 self, uint8 offset) internal pure returns (bytes22 result) {
1298:         if (offset > 2) revert OutOfRangeAccess();
1299:         assembly ("memory-safe") {
1300:             result := and(shl(mul(8, offset), self), shl(80, not(0)))
1301:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1306`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1304:     function replace_24_22(bytes24 self, bytes22 value, uint8 offset) internal pure returns (bytes24 result) {
1305:         bytes22 oldValue = extract_24_22(self, offset);
1306:         assembly ("memory-safe") {
1307:             value := and(value, shl(80, not(0)))
1308:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1314`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1312:     function extract_28_1(bytes28 self, uint8 offset) internal pure returns (bytes1 result) {
1313:         if (offset > 27) revert OutOfRangeAccess();
1314:         assembly ("memory-safe") {
1315:             result := and(shl(mul(8, offset), self), shl(248, not(0)))
1316:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1321`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1319:     function replace_28_1(bytes28 self, bytes1 value, uint8 offset) internal pure returns (bytes28 result) {
1320:         bytes1 oldValue = extract_28_1(self, offset);
1321:         assembly ("memory-safe") {
1322:             value := and(value, shl(248, not(0)))
1323:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1329`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1327:     function extract_28_2(bytes28 self, uint8 offset) internal pure returns (bytes2 result) {
1328:         if (offset > 26) revert OutOfRangeAccess();
1329:         assembly ("memory-safe") {
1330:             result := and(shl(mul(8, offset), self), shl(240, not(0)))
1331:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1336`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1334:     function replace_28_2(bytes28 self, bytes2 value, uint8 offset) internal pure returns (bytes28 result) {
1335:         bytes2 oldValue = extract_28_2(self, offset);
1336:         assembly ("memory-safe") {
1337:             value := and(value, shl(240, not(0)))
1338:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1344`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1342:     function extract_28_4(bytes28 self, uint8 offset) internal pure returns (bytes4 result) {
1343:         if (offset > 24) revert OutOfRangeAccess();
1344:         assembly ("memory-safe") {
1345:             result := and(shl(mul(8, offset), self), shl(224, not(0)))
1346:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1351`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1349:     function replace_28_4(bytes28 self, bytes4 value, uint8 offset) internal pure returns (bytes28 result) {
1350:         bytes4 oldValue = extract_28_4(self, offset);
1351:         assembly ("memory-safe") {
1352:             value := and(value, shl(224, not(0)))
1353:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1359`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1357:     function extract_28_6(bytes28 self, uint8 offset) internal pure returns (bytes6 result) {
1358:         if (offset > 22) revert OutOfRangeAccess();
1359:         assembly ("memory-safe") {
1360:             result := and(shl(mul(8, offset), self), shl(208, not(0)))
1361:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1366`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1364:     function replace_28_6(bytes28 self, bytes6 value, uint8 offset) internal pure returns (bytes28 result) {
1365:         bytes6 oldValue = extract_28_6(self, offset);
1366:         assembly ("memory-safe") {
1367:             value := and(value, shl(208, not(0)))
1368:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1374`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1372:     function extract_28_8(bytes28 self, uint8 offset) internal pure returns (bytes8 result) {
1373:         if (offset > 20) revert OutOfRangeAccess();
1374:         assembly ("memory-safe") {
1375:             result := and(shl(mul(8, offset), self), shl(192, not(0)))
1376:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1381`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1379:     function replace_28_8(bytes28 self, bytes8 value, uint8 offset) internal pure returns (bytes28 result) {
1380:         bytes8 oldValue = extract_28_8(self, offset);
1381:         assembly ("memory-safe") {
1382:             value := and(value, shl(192, not(0)))
1383:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1389`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1387:     function extract_28_10(bytes28 self, uint8 offset) internal pure returns (bytes10 result) {
1388:         if (offset > 18) revert OutOfRangeAccess();
1389:         assembly ("memory-safe") {
1390:             result := and(shl(mul(8, offset), self), shl(176, not(0)))
1391:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1396`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1394:     function replace_28_10(bytes28 self, bytes10 value, uint8 offset) internal pure returns (bytes28 result) {
1395:         bytes10 oldValue = extract_28_10(self, offset);
1396:         assembly ("memory-safe") {
1397:             value := and(value, shl(176, not(0)))
1398:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1404`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1402:     function extract_28_12(bytes28 self, uint8 offset) internal pure returns (bytes12 result) {
1403:         if (offset > 16) revert OutOfRangeAccess();
1404:         assembly ("memory-safe") {
1405:             result := and(shl(mul(8, offset), self), shl(160, not(0)))
1406:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1411`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1409:     function replace_28_12(bytes28 self, bytes12 value, uint8 offset) internal pure returns (bytes28 result) {
1410:         bytes12 oldValue = extract_28_12(self, offset);
1411:         assembly ("memory-safe") {
1412:             value := and(value, shl(160, not(0)))
1413:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1419`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1417:     function extract_28_16(bytes28 self, uint8 offset) internal pure returns (bytes16 result) {
1418:         if (offset > 12) revert OutOfRangeAccess();
1419:         assembly ("memory-safe") {
1420:             result := and(shl(mul(8, offset), self), shl(128, not(0)))
1421:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1426`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1424:     function replace_28_16(bytes28 self, bytes16 value, uint8 offset) internal pure returns (bytes28 result) {
1425:         bytes16 oldValue = extract_28_16(self, offset);
1426:         assembly ("memory-safe") {
1427:             value := and(value, shl(128, not(0)))
1428:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1434`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1432:     function extract_28_20(bytes28 self, uint8 offset) internal pure returns (bytes20 result) {
1433:         if (offset > 8) revert OutOfRangeAccess();
1434:         assembly ("memory-safe") {
1435:             result := and(shl(mul(8, offset), self), shl(96, not(0)))
1436:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1441`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1439:     function replace_28_20(bytes28 self, bytes20 value, uint8 offset) internal pure returns (bytes28 result) {
1440:         bytes20 oldValue = extract_28_20(self, offset);
1441:         assembly ("memory-safe") {
1442:             value := and(value, shl(96, not(0)))
1443:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1449`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1447:     function extract_28_22(bytes28 self, uint8 offset) internal pure returns (bytes22 result) {
1448:         if (offset > 6) revert OutOfRangeAccess();
1449:         assembly ("memory-safe") {
1450:             result := and(shl(mul(8, offset), self), shl(80, not(0)))
1451:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1456`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1454:     function replace_28_22(bytes28 self, bytes22 value, uint8 offset) internal pure returns (bytes28 result) {
1455:         bytes22 oldValue = extract_28_22(self, offset);
1456:         assembly ("memory-safe") {
1457:             value := and(value, shl(80, not(0)))
1458:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1464`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1462:     function extract_28_24(bytes28 self, uint8 offset) internal pure returns (bytes24 result) {
1463:         if (offset > 4) revert OutOfRangeAccess();
1464:         assembly ("memory-safe") {
1465:             result := and(shl(mul(8, offset), self), shl(64, not(0)))
1466:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1471`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1469:     function replace_28_24(bytes28 self, bytes24 value, uint8 offset) internal pure returns (bytes28 result) {
1470:         bytes24 oldValue = extract_28_24(self, offset);
1471:         assembly ("memory-safe") {
1472:             value := and(value, shl(64, not(0)))
1473:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1479`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1477:     function extract_32_1(bytes32 self, uint8 offset) internal pure returns (bytes1 result) {
1478:         if (offset > 31) revert OutOfRangeAccess();
1479:         assembly ("memory-safe") {
1480:             result := and(shl(mul(8, offset), self), shl(248, not(0)))
1481:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1486`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1484:     function replace_32_1(bytes32 self, bytes1 value, uint8 offset) internal pure returns (bytes32 result) {
1485:         bytes1 oldValue = extract_32_1(self, offset);
1486:         assembly ("memory-safe") {
1487:             value := and(value, shl(248, not(0)))
1488:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1494`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1492:     function extract_32_2(bytes32 self, uint8 offset) internal pure returns (bytes2 result) {
1493:         if (offset > 30) revert OutOfRangeAccess();
1494:         assembly ("memory-safe") {
1495:             result := and(shl(mul(8, offset), self), shl(240, not(0)))
1496:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1501`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1499:     function replace_32_2(bytes32 self, bytes2 value, uint8 offset) internal pure returns (bytes32 result) {
1500:         bytes2 oldValue = extract_32_2(self, offset);
1501:         assembly ("memory-safe") {
1502:             value := and(value, shl(240, not(0)))
1503:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1509`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1507:     function extract_32_4(bytes32 self, uint8 offset) internal pure returns (bytes4 result) {
1508:         if (offset > 28) revert OutOfRangeAccess();
1509:         assembly ("memory-safe") {
1510:             result := and(shl(mul(8, offset), self), shl(224, not(0)))
1511:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1516`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1514:     function replace_32_4(bytes32 self, bytes4 value, uint8 offset) internal pure returns (bytes32 result) {
1515:         bytes4 oldValue = extract_32_4(self, offset);
1516:         assembly ("memory-safe") {
1517:             value := and(value, shl(224, not(0)))
1518:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1524`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1522:     function extract_32_6(bytes32 self, uint8 offset) internal pure returns (bytes6 result) {
1523:         if (offset > 26) revert OutOfRangeAccess();
1524:         assembly ("memory-safe") {
1525:             result := and(shl(mul(8, offset), self), shl(208, not(0)))
1526:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1531`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1529:     function replace_32_6(bytes32 self, bytes6 value, uint8 offset) internal pure returns (bytes32 result) {
1530:         bytes6 oldValue = extract_32_6(self, offset);
1531:         assembly ("memory-safe") {
1532:             value := and(value, shl(208, not(0)))
1533:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1539`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1537:     function extract_32_8(bytes32 self, uint8 offset) internal pure returns (bytes8 result) {
1538:         if (offset > 24) revert OutOfRangeAccess();
1539:         assembly ("memory-safe") {
1540:             result := and(shl(mul(8, offset), self), shl(192, not(0)))
1541:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1546`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1544:     function replace_32_8(bytes32 self, bytes8 value, uint8 offset) internal pure returns (bytes32 result) {
1545:         bytes8 oldValue = extract_32_8(self, offset);
1546:         assembly ("memory-safe") {
1547:             value := and(value, shl(192, not(0)))
1548:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1554`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1552:     function extract_32_10(bytes32 self, uint8 offset) internal pure returns (bytes10 result) {
1553:         if (offset > 22) revert OutOfRangeAccess();
1554:         assembly ("memory-safe") {
1555:             result := and(shl(mul(8, offset), self), shl(176, not(0)))
1556:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1561`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1559:     function replace_32_10(bytes32 self, bytes10 value, uint8 offset) internal pure returns (bytes32 result) {
1560:         bytes10 oldValue = extract_32_10(self, offset);
1561:         assembly ("memory-safe") {
1562:             value := and(value, shl(176, not(0)))
1563:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1569`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1567:     function extract_32_12(bytes32 self, uint8 offset) internal pure returns (bytes12 result) {
1568:         if (offset > 20) revert OutOfRangeAccess();
1569:         assembly ("memory-safe") {
1570:             result := and(shl(mul(8, offset), self), shl(160, not(0)))
1571:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1576`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1574:     function replace_32_12(bytes32 self, bytes12 value, uint8 offset) internal pure returns (bytes32 result) {
1575:         bytes12 oldValue = extract_32_12(self, offset);
1576:         assembly ("memory-safe") {
1577:             value := and(value, shl(160, not(0)))
1578:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1584`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1582:     function extract_32_16(bytes32 self, uint8 offset) internal pure returns (bytes16 result) {
1583:         if (offset > 16) revert OutOfRangeAccess();
1584:         assembly ("memory-safe") {
1585:             result := and(shl(mul(8, offset), self), shl(128, not(0)))
1586:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1591`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1589:     function replace_32_16(bytes32 self, bytes16 value, uint8 offset) internal pure returns (bytes32 result) {
1590:         bytes16 oldValue = extract_32_16(self, offset);
1591:         assembly ("memory-safe") {
1592:             value := and(value, shl(128, not(0)))
1593:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1599`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1597:     function extract_32_20(bytes32 self, uint8 offset) internal pure returns (bytes20 result) {
1598:         if (offset > 12) revert OutOfRangeAccess();
1599:         assembly ("memory-safe") {
1600:             result := and(shl(mul(8, offset), self), shl(96, not(0)))
1601:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1606`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1604:     function replace_32_20(bytes32 self, bytes20 value, uint8 offset) internal pure returns (bytes32 result) {
1605:         bytes20 oldValue = extract_32_20(self, offset);
1606:         assembly ("memory-safe") {
1607:             value := and(value, shl(96, not(0)))
1608:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1614`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1612:     function extract_32_22(bytes32 self, uint8 offset) internal pure returns (bytes22 result) {
1613:         if (offset > 10) revert OutOfRangeAccess();
1614:         assembly ("memory-safe") {
1615:             result := and(shl(mul(8, offset), self), shl(80, not(0)))
1616:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1621`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1619:     function replace_32_22(bytes32 self, bytes22 value, uint8 offset) internal pure returns (bytes32 result) {
1620:         bytes22 oldValue = extract_32_22(self, offset);
1621:         assembly ("memory-safe") {
1622:             value := and(value, shl(80, not(0)))
1623:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1629`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1627:     function extract_32_24(bytes32 self, uint8 offset) internal pure returns (bytes24 result) {
1628:         if (offset > 8) revert OutOfRangeAccess();
1629:         assembly ("memory-safe") {
1630:             result := and(shl(mul(8, offset), self), shl(64, not(0)))
1631:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1636`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1634:     function replace_32_24(bytes32 self, bytes24 value, uint8 offset) internal pure returns (bytes32 result) {
1635:         bytes24 oldValue = extract_32_24(self, offset);
1636:         assembly ("memory-safe") {
1637:             value := and(value, shl(64, not(0)))
1638:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1644`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1642:     function extract_32_28(bytes32 self, uint8 offset) internal pure returns (bytes28 result) {
1643:         if (offset > 4) revert OutOfRangeAccess();
1644:         assembly ("memory-safe") {
1645:             result := and(shl(mul(8, offset), self), shl(32, not(0)))
1646:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Packing.sol:1651`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1649:     function replace_32_28(bytes32 self, bytes28 value, uint8 offset) internal pure returns (bytes32 result) {
1650:         bytes28 oldValue = extract_32_28(self, offset);
1651:         assembly ("memory-safe") {
1652:             value := and(value, shl(32, not(0)))
1653:             result := xor(self, shr(mul(8, offset), xor(oldValue, value)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Panic.sol:51`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
49:     /// the internal constants with predefined codes.
50:     function panic(uint256 code) internal pure {
51:         assembly ("memory-safe") {
52:             mstore(0x00, 0x4e487b71)
53:             mstore(0x20, code)
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `utils/RLP.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Rule confidence**: low
- **Rule rationale**: File size is a rough proxy for deployed bytecode size. A raised max contract size would relax rather than break constraints, so this is a watch point only.
- **Related fork candidates**: EIP-7907 (meter and increase contract code size, candidate)
- **Manual review required**: Yes

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/RLP.sol:145`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
143:      */
144:     function encode(bool input) internal pure returns (bytes memory result) {
145:         assembly ("memory-safe") {
146:             result := mload(0x40)
147:             mstore(result, 0x01) // length of the encoded data: 1 byte
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/RLP.sol:160`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
158:      */
159:     function encode(address input) internal pure returns (bytes memory result) {
160:         assembly ("memory-safe") {
161:             result := mload(0x40)
162:             mstore(result, 0x15) // length of the encoded data: 1 (prefix) + 0x14 (address)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/RLP.sol:175`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
173:     function encode(uint256 input) internal pure returns (bytes memory result) {
174:         if (input < SHORT_OFFSET) {
175:             assembly ("memory-safe") {
176:                 result := mload(0x40)
177:                 mstore(result, 0x01) // length of the encoded data: 1 byte
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/RLP.sol:183`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
181:         } else {
182:             uint256 length = Math.log256(input) + 1;
183:             assembly ("memory-safe") {
184:                 result := mload(0x40)
185:                 mstore(result, add(length, 1)) // length of the encoded data: 1 (prefix) + length
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/RLP.sol:199`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
197:      */
198:     function encode(bytes32 input) internal pure returns (bytes memory result) {
199:         assembly ("memory-safe") {
200:             result := mload(0x40)
201:             mstore(result, 0x21) // length of the encoded data: 1 (prefix) + 0x20
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/RLP.sol:238`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
236:             // Encode "short-bytes" as
237:             // [ offset + input.length | input ]
238:             assembly ("memory-safe") {
239:                 result := mload(0x40)
240:                 mstore(result, add(length, 1)) // length of the encoded data: 1 (prefix) + input.length
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/RLP.sol:249`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
247:             // [ SHORT_THRESHOLD + offset + input.length.length | input.length | input ]
248:             uint256 lenlength = Math.log256(length) + 1;
249:             assembly ("memory-safe") {
250:                 result := mload(0x40)
251:                 mstore(result, add(add(length, lenlength), 1)) // length of the encoded data: 1 (prefix) + input.length.length + input.length
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/RLP.sol:363`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
361:         // Start a buffer in the unallocated space
362:         uint256 ptr;
363:         assembly ("memory-safe") {
364:             list := mload(0x40)
365:             ptr := add(list, 0x20)
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/RLP.sol:369`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
367: 
368:         // Get all items in order, and push them to the buffer
369:         for (uint256 currentOffset = listOffset; currentOffset < itemLength; ptr += 0x20) {
370:             (uint256 elementOffset, uint256 elementLength, ) = _decodeLength(item.slice(currentOffset));
371:             Memory.Slice element = item.slice(currentOffset, elementLength + elementOffset);
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/RLP.sol:375`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
373: 
374:             // Write item to the buffer
375:             assembly ("memory-safe") {
376:                 mstore(ptr, element)
377:             }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/RLP.sol:381`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
379: 
380:         // write list length and reserve space
381:         assembly ("memory-safe") {
382:             mstore(list, div(sub(ptr, add(list, 0x20)), 0x20))
383:             mstore(0x40, ptr)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/RelayedCall.sol:16`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
14:  * the target only sees the unprivileged relay address as `msg.sender`.
15:  *
16:  * For example, instead of `target.call(data)` where the target sees this contract as `msg.sender`, use
17:  * {relayCall} where the target sees a relay address as `msg.sender`.
18:  *
```

### [Low] glamsterdam-eth-transfer-assumption

- **Location**: `utils/RelayedCall.sol:46`
- **Review note**: Native ETH transfer assumption. Review ETH transfer assumptions against proposed native ETH transfer logs and any gas repricing that may affect transfer-style patterns.
- **Rule confidence**: medium
- **Rule rationale**: transfer()/send() forward a fixed 2300 gas stipend and value-bearing calls embed gas-cost assumptions. Gas repricing candidates and native ETH transfer logs directly touch these patterns, so a keyword match is usually relevant.
- **Related fork candidates**: EIP-7708 (ETH transfers emit a log, candidate), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
44:         bytes32 salt
45:     ) internal returns (bool, bytes memory) {
46:         return getRelayer(salt).call{value: value}(abi.encodePacked(target, data));
47:     }
48: 
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/RelayedCall.sol:108`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
106:         // 0x0046 | f3          | return         |
107: 
108:         assembly ("memory-safe") {
109:             let fmp := mload(0x40)
110: 
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/ShortStrings.sol:67`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
65:         // using `new string(len)` would work locally but is not memory safe.
66:         string memory str = new string(0x20);
67:         assembly ("memory-safe") {
68:             mstore(str, len)
69:             mstore(add(str, 0x20), sstr)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SlotDerivation.sol:46`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
44:      */
45:     function erc7201Slot(string memory namespace) internal pure returns (bytes32 slot) {
46:         assembly ("memory-safe") {
47:             mstore(0x00, sub(keccak256(add(namespace, 0x20), mload(namespace)), 1))
48:             slot := and(keccak256(0x00, 0x20), not(0xff))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SlotDerivation.sol:65`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
63:      */
64:     function deriveArray(bytes32 slot) internal pure returns (bytes32 result) {
65:         assembly ("memory-safe") {
66:             mstore(0x00, slot)
67:             result := keccak256(0x00, 0x20)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SlotDerivation.sol:75`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
73:      */
74:     function deriveMapping(bytes32 slot, address key) internal pure returns (bytes32 result) {
75:         assembly ("memory-safe") {
76:             mstore(0x00, and(key, shr(96, not(0))))
77:             mstore(0x20, slot)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SlotDerivation.sol:86`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
84:      */
85:     function deriveMapping(bytes32 slot, bool key) internal pure returns (bytes32 result) {
86:         assembly ("memory-safe") {
87:             mstore(0x00, iszero(iszero(key)))
88:             mstore(0x20, slot)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SlotDerivation.sol:97`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
95:      */
96:     function deriveMapping(bytes32 slot, bytes32 key) internal pure returns (bytes32 result) {
97:         assembly ("memory-safe") {
98:             mstore(0x00, key)
99:             mstore(0x20, slot)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SlotDerivation.sol:108`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
106:      */
107:     function deriveMapping(bytes32 slot, uint256 key) internal pure returns (bytes32 result) {
108:         assembly ("memory-safe") {
109:             mstore(0x00, key)
110:             mstore(0x20, slot)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SlotDerivation.sol:119`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
117:      */
118:     function deriveMapping(bytes32 slot, int256 key) internal pure returns (bytes32 result) {
119:         assembly ("memory-safe") {
120:             mstore(0x00, key)
121:             mstore(0x20, slot)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SlotDerivation.sol:130`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
128:      */
129:     function deriveMapping(bytes32 slot, string memory key) internal pure returns (bytes32 result) {
130:         assembly ("memory-safe") {
131:             let length := mload(key)
132:             let begin := add(key, 0x20)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/SlotDerivation.sol:145`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
143:      */
144:     function deriveMapping(bytes32 slot, bytes memory key) internal pure returns (bytes32 result) {
145:         assembly ("memory-safe") {
146:             let length := mload(key)
147:             let begin := add(key, 0x20)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/StorageSlot.sol:11`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
9:  *
10:  * Storage slots are often used to avoid storage conflict when dealing with upgradeable contracts.
11:  * This library helps with reading and writing to such slots without the need for inline assembly.
12:  *
13:  * The functions in this library return Slot structs that contain a `value` member that can be used to read or write.
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/StorageSlot.sol:67`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
65:      */
66:     function getAddressSlot(bytes32 slot) internal pure returns (AddressSlot storage r) {
67:         assembly ("memory-safe") {
68:             r.slot := slot
69:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/StorageSlot.sol:76`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
74:      */
75:     function getBooleanSlot(bytes32 slot) internal pure returns (BooleanSlot storage r) {
76:         assembly ("memory-safe") {
77:             r.slot := slot
78:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/StorageSlot.sol:85`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
83:      */
84:     function getBytes32Slot(bytes32 slot) internal pure returns (Bytes32Slot storage r) {
85:         assembly ("memory-safe") {
86:             r.slot := slot
87:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/StorageSlot.sol:94`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
92:      */
93:     function getUint256Slot(bytes32 slot) internal pure returns (Uint256Slot storage r) {
94:         assembly ("memory-safe") {
95:             r.slot := slot
96:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/StorageSlot.sol:103`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
101:      */
102:     function getInt256Slot(bytes32 slot) internal pure returns (Int256Slot storage r) {
103:         assembly ("memory-safe") {
104:             r.slot := slot
105:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/StorageSlot.sol:112`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
110:      */
111:     function getStringSlot(bytes32 slot) internal pure returns (StringSlot storage r) {
112:         assembly ("memory-safe") {
113:             r.slot := slot
114:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/StorageSlot.sol:121`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
119:      */
120:     function getStringSlot(string storage store) internal pure returns (StringSlot storage r) {
121:         assembly ("memory-safe") {
122:             r.slot := store.slot
123:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/StorageSlot.sol:130`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
128:      */
129:     function getBytesSlot(bytes32 slot) internal pure returns (BytesSlot storage r) {
130:         assembly ("memory-safe") {
131:             r.slot := slot
132:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/StorageSlot.sol:139`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
137:      */
138:     function getBytesSlot(bytes storage store) internal pure returns (BytesSlot storage r) {
139:         assembly ("memory-safe") {
140:             r.slot := store.slot
141:         }
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `utils/Strings.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Rule confidence**: low
- **Rule rationale**: File size is a rough proxy for deployed bytecode size. A raised max contract size would relax rather than break constraints, so this is a watch point only.
- **Related fork candidates**: EIP-7907 (meter and increase contract code size, candidate)
- **Manual review required**: Yes

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Strings.sol:47`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
45:             string memory buffer = new string(length);
46:             uint256 ptr;
47:             assembly ("memory-safe") {
48:                 ptr := add(add(buffer, 0x20), length)
49:             }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Strings.sol:50`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
48:                 ptr := add(add(buffer, 0x20), length)
49:             }
50:             while (true) {
51:                 ptr--;
52:                 assembly ("memory-safe") {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Strings.sol:52`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
50:             while (true) {
51:                 ptr--;
52:                 assembly ("memory-safe") {
53:                     mstore8(ptr, byte(mod(value, 10), HEX_DIGITS))
54:                 }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Strings.sol:86`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
84:         buffer[0] = "0";
85:         buffer[1] = "x";
86:         for (uint256 i = 2 * length + 1; i > 1; --i) {
87:             buffer[i] = HEX_DIGITS[localValue & 0xf];
88:             localValue >>= 4;
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Strings.sol:113`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
111:         // hash the hex part of buffer (skip length + 2 bytes, length 40)
112:         uint256 hashValue;
113:         assembly ("memory-safe") {
114:             hashValue := shr(96, keccak256(add(buffer, 0x22), 40))
115:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Strings.sol:117`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
115:         }
116: 
117:         for (uint256 i = 41; i > 1; --i) {
118:             // possible values for buffer[i] are 48 (0) to 57 (9) and 97 (a) to 102 (f)
119:             if (hashValue & 0xf > 7 && uint8(buffer[i]) > 96) {
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Strings.sol:136`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
134:             buffer[0] = "0";
135:             buffer[1] = "x";
136:             for (uint256 i = 0; i < input.length; ++i) {
137:                 uint8 v = uint8(input[i]);
138:                 buffer[2 * i + 2] = HEX_DIGITS[v >> 4];
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Strings.sol:213`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
211: 
212:         uint256 result = 0;
213:         for (uint256 i = begin; i < end; ++i) {
214:             uint8 chr = _tryParseChr(bytes1(_unsafeReadBytesOffset(buffer, i)));
215:             if (chr > 9) return (false, 0);
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Strings.sol:365`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
363: 
364:         uint256 result = 0;
365:         for (uint256 i = begin + offset; i < end; ++i) {
366:             uint8 chr = _tryParseChr(bytes1(_unsafeReadBytesOffset(buffer, i)));
367:             if (chr > 15) return (false, 0);
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Strings.sol:468`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
466:         // each character written.
467:         bytes memory output;
468:         assembly ("memory-safe") {
469:             output := mload(0x40)
470:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/Strings.sol:473`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
471:         uint256 outputLength = 0;
472: 
473:         for (uint256 i = 0; i < buffer.length; ++i) {
474:             uint8 char = uint8(bytes1(_unsafeReadBytesOffset(buffer, i)));
475:             if (((SPECIAL_CHARS_LOOKUP & (1 << char)) != 0)) {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Strings.sol:499`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
497:         }
498:         // write the actual length and reserve memory
499:         assembly ("memory-safe") {
500:             mstore(output, outputLength)
501:             mstore(0x40, add(output, add(outputLength, 0x20)))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Strings.sol:511`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
509:      *
510:      * NOTE: making this function internal would mean it could be used with memory unsafe offset, and marking the
511:      * assembly block as such would prevent some optimizations.
512:      */
513:     function _unsafeReadBytesOffset(bytes memory buffer, uint256 offset) private pure returns (bytes32 value) {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Strings.sol:515`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
513:     function _unsafeReadBytesOffset(bytes memory buffer, uint256 offset) private pure returns (bytes32 value) {
514:         // This is not memory safe in the general case, but all calls to this private function are within bounds.
515:         assembly ("memory-safe") {
516:             value := mload(add(add(buffer, 0x20), offset))
517:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Strings.sol:524`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
522:      *
523:      * NOTE: making this function internal would mean it could be used with memory unsafe offset, and marking the
524:      * assembly block as such would prevent some optimizations.
525:      */
526:     function _unsafeWriteBytesOffset(bytes memory buffer, uint256 offset, bytes1 value) private pure {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/Strings.sol:528`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
526:     function _unsafeWriteBytesOffset(bytes memory buffer, uint256 offset, bytes1 value) private pure {
527:         // This is not memory safe in the general case, but all calls to this private function are within bounds.
528:         assembly ("memory-safe") {
529:             mstore8(add(add(buffer, 0x20), offset), shr(248, value))
530:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/TransientSlot.sol:11`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
9:  *
10:  * Transient slots are often used to store temporary values that are removed after the current transaction.
11:  * This library helps with reading and writing to such slots without the need for inline assembly.
12:  *
13:  *  * Example reading and writing values using transient storage:
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/TransientSlot.sol:98`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
96:      */
97:     function tload(AddressSlot slot) internal view returns (address value) {
98:         assembly ("memory-safe") {
99:             value := tload(slot)
100:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/TransientSlot.sol:107`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
105:      */
106:     function tstore(AddressSlot slot, address value) internal {
107:         assembly ("memory-safe") {
108:             tstore(slot, value)
109:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/TransientSlot.sol:116`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
114:      */
115:     function tload(BooleanSlot slot) internal view returns (bool value) {
116:         assembly ("memory-safe") {
117:             value := tload(slot)
118:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/TransientSlot.sol:125`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
123:      */
124:     function tstore(BooleanSlot slot, bool value) internal {
125:         assembly ("memory-safe") {
126:             tstore(slot, value)
127:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/TransientSlot.sol:134`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
132:      */
133:     function tload(Bytes32Slot slot) internal view returns (bytes32 value) {
134:         assembly ("memory-safe") {
135:             value := tload(slot)
136:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/TransientSlot.sol:143`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
141:      */
142:     function tstore(Bytes32Slot slot, bytes32 value) internal {
143:         assembly ("memory-safe") {
144:             tstore(slot, value)
145:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/TransientSlot.sol:152`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
150:      */
151:     function tload(Uint256Slot slot) internal view returns (uint256 value) {
152:         assembly ("memory-safe") {
153:             value := tload(slot)
154:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/TransientSlot.sol:161`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
159:      */
160:     function tstore(Uint256Slot slot, uint256 value) internal {
161:         assembly ("memory-safe") {
162:             tstore(slot, value)
163:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/TransientSlot.sol:170`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
168:      */
169:     function tload(Int256Slot slot) internal view returns (int256 value) {
170:         assembly ("memory-safe") {
171:             value := tload(slot)
172:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/TransientSlot.sol:179`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
177:      */
178:     function tstore(Int256Slot slot, int256 value) internal {
179:         assembly ("memory-safe") {
180:             tstore(slot, value)
181:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/ECDSA.sol:71`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
69:             // ecrecover takes the signature parameters, and the only way to get them
70:             // currently is to use assembly.
71:             assembly ("memory-safe") {
72:                 r := mload(add(signature, 0x20))
73:                 s := mload(add(signature, 0x40))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/ECDSA.sol:95`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
93:             // ecrecover takes the signature parameters, calldata slices would work here, but are
94:             // significantly more expensive (length check) than using calldataload in assembly.
95:             assembly ("memory-safe") {
96:                 r := calldataload(signature.offset)
97:                 s := calldataload(add(signature.offset, 0x20))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/ECDSA.sol:218`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
216:      */
217:     function parse(bytes memory signature) internal pure returns (uint8 v, bytes32 r, bytes32 s) {
218:         assembly ("memory-safe") {
219:             // Check the signature length
220:             switch mload(signature)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/ECDSA.sol:246`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
244:      */
245:     function parseCalldata(bytes calldata signature) internal pure returns (uint8 v, bytes32 r, bytes32 s) {
246:         assembly ("memory-safe") {
247:             // Check the signature length
248:             switch signature.length
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/Hashes.sol:25`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
23:      */
24:     function efficientKeccak256(bytes32 a, bytes32 b) internal pure returns (bytes32 value) {
25:         assembly ("memory-safe") {
26:             mstore(0x00, a)
27:             mstore(0x20, b)
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `utils/cryptography/MerkleProof.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Rule confidence**: low
- **Rule rationale**: File size is a rough proxy for deployed bytecode size. A raised max contract size would relax rather than break constraints, so this is a watch point only.
- **Related fork candidates**: EIP-7907 (meter and increase contract code size, candidate)
- **Manual review required**: Yes

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/MerkleProof.sol:59`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
57:     function processProof(bytes32[] memory proof, bytes32 leaf) internal pure returns (bytes32) {
58:         bytes32 computedHash = leaf;
59:         for (uint256 i = 0; i < proof.length; i++) {
60:             computedHash = Hashes.commutativeKeccak256(computedHash, proof[i]);
61:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/MerkleProof.sol:96`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
94:     ) internal view returns (bytes32) {
95:         bytes32 computedHash = leaf;
96:         for (uint256 i = 0; i < proof.length; i++) {
97:             computedHash = hasher(computedHash, proof[i]);
98:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/MerkleProof.sol:124`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
122:     function processProofCalldata(bytes32[] calldata proof, bytes32 leaf) internal pure returns (bytes32) {
123:         bytes32 computedHash = leaf;
124:         for (uint256 i = 0; i < proof.length; i++) {
125:             computedHash = Hashes.commutativeKeccak256(computedHash, proof[i]);
126:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/MerkleProof.sol:161`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
159:     ) internal view returns (bytes32) {
160:         bytes32 computedHash = leaf;
161:         for (uint256 i = 0; i < proof.length; i++) {
162:             computedHash = hasher(computedHash, proof[i]);
163:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/MerkleProof.sol:232`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
230:             // - depending on the flag, either another value from the "main queue" (merging branches) or an element from the
231:             //   `proof` array.
232:             for (uint256 i = 0; i < proofFlagsLen; i++) {
233:                 bytes32 a = leafPos < leavesLen ? leaves[leafPos++] : hashes[hashPos++];
234:                 bytes32 b = proofFlags[i]
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/MerkleProof.sol:319`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
317:             // - depending on the flag, either another value from the "main queue" (merging branches) or an element from the
318:             //   `proof` array.
319:             for (uint256 i = 0; i < proofFlagsLen; i++) {
320:                 bytes32 a = leafPos < leavesLen ? leaves[leafPos++] : hashes[hashPos++];
321:                 bytes32 b = proofFlags[i]
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/MerkleProof.sol:404`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
402:             // - depending on the flag, either another value from the "main queue" (merging branches) or an element from the
403:             //   `proof` array.
404:             for (uint256 i = 0; i < proofFlagsLen; i++) {
405:                 bytes32 a = leafPos < leavesLen ? leaves[leafPos++] : hashes[hashPos++];
406:                 bytes32 b = proofFlags[i]
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/MerkleProof.sol:491`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
489:             // - depending on the flag, either another value from the "main queue" (merging branches) or an element from the
490:             //   `proof` array.
491:             for (uint256 i = 0; i < proofFlagsLen; i++) {
492:                 bytes32 a = leafPos < leavesLen ? leaves[leafPos++] : hashes[hashPos++];
493:                 bytes32 b = proofFlags[i]
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/MessageHashUtils.sol:33`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
31:      */
32:     function toEthSignedMessageHash(bytes32 messageHash) internal pure returns (bytes32 digest) {
33:         assembly ("memory-safe") {
34:             mstore(0x00, "\x19Ethereum Signed Message:\n32") // 32 is the bytes-length of messageHash
35:             mstore(0x1c, messageHash) // 0x1c (28) is the length of the prefix
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/MessageHashUtils.sol:75`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
73:         bytes32 messageHash
74:     ) internal pure returns (bytes32 digest) {
75:         assembly ("memory-safe") {
76:             mstore(0x00, hex"19_00")
77:             mstore(0x02, shl(96, validator))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/MessageHashUtils.sol:93`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
91:      */
92:     function toTypedDataHash(bytes32 domainSeparator, bytes32 structHash) internal pure returns (bytes32 digest) {
93:         assembly ("memory-safe") {
94:             let ptr := mload(0x40)
95:             mstore(ptr, hex"19_01")
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/MessageHashUtils.sol:147`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
145:         bytes32 domainTypeHash = toDomainTypeHash(fields);
146: 
147:         assembly ("memory-safe") {
148:             // align fields to the right for easy processing
149:             fields := shr(248, fields)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/MessageHashUtils.sol:185`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
183:         if (fields & 0x20 == 0x20) revert ERC5267ExtensionsNotSupported();
184: 
185:         assembly ("memory-safe") {
186:             // align fields to the right for easy processing
187:             fields := shr(248, fields)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/P256.sol:117`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
115:      */
116:     function _rip7212(bytes32 h, bytes32 r, bytes32 s, bytes32 qx, bytes32 qy) private view returns (bool isValid) {
117:         assembly ("memory-safe") {
118:             // Use the free memory pointer without updating it at the end of the function
119:             let ptr := mload(0x40)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/P256.sol:189`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
187:      */
188:     function isValidPublicKey(bytes32 x, bytes32 y) internal pure returns (bool result) {
189:         assembly ("memory-safe") {
190:             let p := P
191:             let lhs := mulmod(y, y, p) // y^2
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/P256.sol:217`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
215:         uint256 p = P; // cache P on the stack
216:         uint256 zinv = Math.invModPrime(jz, p);
217:         assembly ("memory-safe") {
218:             let zzinv := mulmod(zinv, zinv, p)
219:             ax := mulmod(jx, zzinv, p)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/P256.sol:241`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
239:         uint256 z2
240:     ) private pure returns (uint256 rx, uint256 ry, uint256 rz) {
241:         assembly ("memory-safe") {
242:             let p := P
243:             let z1 := mload(add(p1, 0x40))
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/P256.sol:301`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
299:      */
300:     function _jDouble(uint256 x, uint256 y, uint256 z) private pure returns (uint256 rx, uint256 ry, uint256 rz) {
301:         assembly ("memory-safe") {
302:             let p := P
303:             let yy := mulmod(y, y, p)
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/P256.sol:336`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
334:         uint256 z = 0;
335:         unchecked {
336:             for (uint256 i = 0; i < 128; ++i) {
337:                 if (z > 0) {
338:                     (x, y, z) = _jDouble(x, y, z);
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/RSA.sol:64`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
62: 
63:             // Verify that s < n to ensure there's only one valid signature for a given message
64:             for (uint256 i = 0; i < length; i += 0x20) {
65:                 uint256 p = Math.min(i, length - 0x20);
66:                 bytes32 sp = _unsafeReadBytes32(s, p);
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/RSA.sol:130`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
128:             // use the padding to manipulate the message in order to create a valid signature out of
129:             // multiple valid signatures.
130:             for (uint256 i = 2; i < paddingEnd; ++i) {
131:                 if (bytes1(_unsafeReadBytes32(buffer, i)) != 0xFF) {
132:                     return false;
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/RSA.sol:150`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
148:         // Memory safeness is guaranteed as long as the provided `array` is a Solidity-allocated bytes array
149:         // and `offset` is within bounds. This is the case for all calls to this private function from {pkcs1Sha256}.
150:         assembly ("memory-safe") {
151:             result := mload(add(add(array, 0x20), offset))
152:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/SignatureChecker.sol:72`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
70:         uint256 length = signature.length;
71: 
72:         assembly ("memory-safe") {
73:             // Encoded calldata is :
74:             // [ 0x00 - 0x03 ] <selector>
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/SignatureChecker.sol:98`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
96:         uint256 length = signature.length;
97: 
98:         assembly ("memory-safe") {
99:             // Encoded calldata is :
100:             // [ 0x00 - 0x03 ] <selector>
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/SignatureChecker.sol:142`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
140:             return isValidSignatureNow(address(bytes20(signer)), hash, signature);
141:         } else {
142:             (bool success, bytes memory result) = address(bytes20(signer)).staticcall(
143:                 abi.encodeCall(IERC7913SignatureVerifier.verify, (signer.slice(20), hash, signature))
144:             );
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/SignatureChecker.sol:170`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
168:         bytes32 lastId = bytes32(0);
169: 
170:         for (uint256 i = 0; i < signers.length; ++i) {
171:             bytes memory signer = signers[i];
172: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/SignatureChecker.sol:183`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
181:                 // If this signer id is not greater than all the previous ones, verify that it is not a duplicate of a previous one
182:                 // This loop is never executed if the signers are ordered by id.
183:                 for (uint256 j = 0; j < i; ++j) {
184:                     if (id == keccak256(signers[j])) return false;
185:                 }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/TrieProof.sol:114`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
112:         // Traverse proof
113:         uint256 keyIndex = 0;
114:         for (uint256 i = 0; i < proof.length; ++i) {
115:             // validates the encoded node matches the expected node id
116:             bytes memory encoded = proof[i];
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/TrieProof.sol:131`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
129: 
130:             // decode the current node as an RLP list, and process it
131:             for (Memory.Slice[] memory decoded = encoded.decodeList(); ; ) {
132:                 if (decoded.length == BRANCH_NODE_LENGTH) {
133:                     // If we've consumed the entire key, the value must be in the last slot
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/TrieProof.sol:247`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
245: 
246:     function _emptyBytesMemory() private pure returns (bytes memory result) {
247:         assembly ("memory-safe") {
248:             result := 0x60 // mload(0x60) is always 0
249:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/WebAuthn.sol:136`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
134:         uint256 typeIndex
135:     ) private pure returns (bool success) {
136:         assembly ("memory-safe") {
137:             success := and(
138:                 // clientDataJson.length >= typeIndex + 21
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/cryptography/WebAuthn.sol:240`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
238:      */
239:     function tryDecodeAuth(bytes calldata input) internal pure returns (bool success, WebAuthnAuth calldata auth) {
240:         assembly ("memory-safe") {
241:             auth := input.offset
242:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/draft-ERC7739Utils.sol:176`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
174:         } else if (buffer[buffer.length - 1] == bytes1(")")) {
175:             // Implicit mode: read contentsName from the beginning, and keep the complete descr
176:             for (uint256 i = 0; i < buffer.length; ++i) {
177:                 bytes1 current = buffer[i];
178:                 if (current == bytes1("(")) {
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/draft-ERC7739Utils.sol:190`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
188:         } else {
189:             // Explicit mode: read contentsName from the end, and remove it from the descr
190:             for (uint256 i = buffer.length; i > 0; --i) {
191:                 bytes1 current = buffer[i - 1];
192:                 if (current == bytes1(")")) {
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/signers/MultiSignerERC7913.sol:126`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
124:      */
125:     function _addSigners(bytes[] memory newSigners) internal virtual {
126:         for (uint256 i = 0; i < newSigners.length; ++i) {
127:             bytes memory signer = newSigners[i];
128:             require(signer.length >= 20, MultiSignerERC7913InvalidSigner(signer));
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/signers/MultiSignerERC7913.sol:143`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
141:      */
142:     function _removeSigners(bytes[] memory oldSigners) internal virtual {
143:         for (uint256 i = 0; i < oldSigners.length; ++i) {
144:             bytes memory signer = oldSigners[i];
145:             require(_signers.remove(signer), MultiSignerERC7913NonexistentSigner(signer));
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/signers/MultiSignerERC7913.sol:244`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
242:         bytes[] memory signatures
243:     ) internal view virtual returns (bool valid) {
244:         for (uint256 i = 0; i < signers.length; ++i) {
245:             if (!isSigner(signers[i])) {
246:                 return false;
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/signers/MultiSignerERC7913Weighted.sol:106`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
104:         uint256 extraWeightAdded = 0;
105:         uint256 extraWeightRemoved = 0;
106:         for (uint256 i = 0; i < signers.length; ++i) {
107:             bytes memory signer = signers[i];
108:             require(isSigner(signer), MultiSignerERC7913NonexistentSigner(signer));
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/signers/MultiSignerERC7913Weighted.sol:161`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
159:         unchecked {
160:             uint64 extraWeightRemoved = 0;
161:             for (uint256 i = 0; i < signers.length; ++i) {
162:                 bytes memory signer = signers[i];
163: 
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/cryptography/signers/MultiSignerERC7913Weighted.sol:201`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
199:         unchecked {
200:             uint64 weight = 0;
201:             for (uint256 i = 0; i < signers.length; ++i) {
202:                 // Overflow impossible: weight values are bounded by uint64 and economic constraints
203:                 weight += signerWeight(signers[i]);
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/draft-InteroperableAddress.sol:229`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
227:     function _readBytes2(bytes memory buffer, uint256 offset) private pure returns (bytes2 value) {
228:         // This is not memory safe in the general case, but all calls to this private function are within bounds.
229:         assembly ("memory-safe") {
230:             value := shl(240, shr(240, mload(add(add(buffer, 0x20), offset))))
231:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/draft-InteroperableAddress.sol:235`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
233: 
234:     function _readBytes2Calldata(bytes calldata buffer, uint256 offset) private pure returns (bytes2 value) {
235:         assembly ("memory-safe") {
236:             value := shl(240, shr(240, calldataload(add(buffer.offset, offset))))
237:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/draft-InteroperableAddress.sol:241`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
239: 
240:     function _emptyBytesMemory() private pure returns (bytes memory result) {
241:         assembly ("memory-safe") {
242:             result := 0x60 // mload(0x60) is always 0
243:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/introspection/ERC165Checker.sol:62`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
60:         if (supportsERC165(account)) {
61:             // query support of each interface in interfaceIds
62:             for (uint256 i = 0; i < interfaceIds.length; i++) {
63:                 interfaceIdsSupported[i] = supportsERC165InterfaceUnchecked(account, interfaceIds[i]);
64:             }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/introspection/ERC165Checker.sol:86`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
84: 
85:         // query support of each interface in interfaceIds
86:         for (uint256 i = 0; i < interfaceIds.length; i++) {
87:             if (!supportsERC165InterfaceUnchecked(account, interfaceIds[i])) {
88:                 return false;
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/introspection/ERC165Checker.sol:132`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
130:         bytes4 selector = IERC165.supportsInterface.selector;
131: 
132:         assembly ("memory-safe") {
133:             mstore(0x00, selector)
134:             mstore(0x04, interfaceId)
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `utils/math/Math.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Rule confidence**: low
- **Rule rationale**: File size is a rough proxy for deployed bytecode size. A raised max contract size would relax rather than break constraints, so this is a watch point only.
- **Related fork candidates**: EIP-7907 (meter and increase contract code size, candidate)
- **Manual review required**: Yes

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/math/Math.sol:26`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
24:      */
25:     function add512(uint256 a, uint256 b) internal pure returns (uint256 high, uint256 low) {
26:         assembly ("memory-safe") {
27:             low := add(a, b)
28:             high := lt(low, a)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/math/Math.sol:41`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
39:         // the Chinese Remainder Theorem to reconstruct the 512 bit result. The result is stored in two 256
40:         // variables such that product = high * 2²⁵⁶ + low.
41:         assembly ("memory-safe") {
42:             let mm := mulmod(a, b, not(0))
43:             low := mul(a, b)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/math/Math.sol:76`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
74:         unchecked {
75:             uint256 c = a * b;
76:             assembly ("memory-safe") {
77:                 // Only true when the multiplication doesn't overflow
78:                 // (c / a == b) || (a == 0)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/math/Math.sol:92`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
90:         unchecked {
91:             success = b > 0;
92:             assembly ("memory-safe") {
93:                 // The `DIV` opcode returns zero when the denominator is 0.
94:                 result := div(a, b)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/math/Math.sol:105`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
103:         unchecked {
104:             success = b > 0;
105:             assembly ("memory-safe") {
106:                 // The `MOD` opcode returns zero when the denominator is 0.
107:                 result := mod(a, b)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/math/Math.sol:229`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
227:             // Make division exact by subtracting the remainder from [high low].
228:             uint256 remainder;
229:             assembly ("memory-safe") {
230:                 // Compute remainder using mulmod.
231:                 remainder := mulmod(x, y, denominator)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/math/Math.sol:242`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
240: 
241:             uint256 twos = denominator & (0 - denominator);
242:             assembly ("memory-safe") {
243:                 // Divide denominator by twos.
244:                 denominator := div(denominator, twos)
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/math/Math.sol:338`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
336:             int256 y = 1;
337: 
338:             while (remainder != 0) {
339:                 uint256 quotient = gcd / remainder;
340: 
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/math/Math.sol:413`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
411:     function tryModExp(uint256 b, uint256 e, uint256 m) internal view returns (bool success, uint256 result) {
412:         if (m == 0) return (false, 0);
413:         assembly ("memory-safe") {
414:             let ptr := mload(0x40)
415:             // | Offset    | Content    | Content (Hex)                                                      |
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/math/Math.sol:463`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
461:         result = abi.encodePacked(b.length, e.length, mLen, b, e, m);
462: 
463:         assembly ("memory-safe") {
464:             let dataPtr := add(result, 0x20)
465:             // Write result on top of args to avoid allocating extra memory.
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/math/Math.sol:480`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
478:     function _zeroBytes(bytes memory buffer) private pure returns (bool) {
479:         uint256 chunk;
480:         for (uint256 i = 0; i < buffer.length; i += 0x20) {
481:             // See _unsafeReadBytesOffset from utils/Bytes.sol
482:             assembly ("memory-safe") {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/math/Math.sol:482`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
480:         for (uint256 i = 0; i < buffer.length; i += 0x20) {
481:             // See _unsafeReadBytesOffset from utils/Bytes.sol
482:             assembly ("memory-safe") {
483:                 chunk := mload(add(add(buffer, 0x20), i))
484:             }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/math/Math.sol:655`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
653:         //
654:         // The lookup table is represented as a 32-byte value with the MSB positions for 0-15 in the first 16 bytes (most significant half).
655:         assembly ("memory-safe") {
656:             r := or(r, byte(shr(r, x), 0x0000010102020202030303030303030300000000000000000000000000000000))
657:         }
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `utils/math/SafeCast.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Rule confidence**: low
- **Rule rationale**: File size is a rough proxy for deployed bytecode size. A raised max contract size would relax rather than break constraints, so this is a watch point only.
- **Related fork candidates**: EIP-7907 (meter and increase contract code size, candidate)
- **Manual review required**: Yes

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/math/SafeCast.sol:1158`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1156:      */
1157:     function toUint(bool b) internal pure returns (uint256 u) {
1158:         assembly ("memory-safe") {
1159:             u := iszero(iszero(b))
1160:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/Accumulators.sol:101`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
99:     /// @dev Flatten all the bytes entries in an Accumulator into a single buffer
100:     function flatten(Accumulator memory self) internal pure returns (bytes memory result) {
101:         assembly ("memory-safe") {
102:             result := mload(0x40)
103:             let ptr := add(result, 0x20)
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/Accumulators.sol:121`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
119: 
120:     function _asPtr(AccumulatorEntry memory item) private pure returns (Memory.Pointer ptr) {
121:         assembly ("memory-safe") {
122:             ptr := item
123:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/Accumulators.sol:127`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
125: 
126:     function _asAccumulatorEntry(Memory.Pointer ptr) private pure returns (AccumulatorEntry memory item) {
127:         assembly ("memory-safe") {
128:             item := ptr
129:         }
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `utils/structs/Checkpoints.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Rule confidence**: low
- **Rule rationale**: File size is a rough proxy for deployed bytecode size. A raised max contract size would relax rather than break constraints, so this is a watch point only.
- **Related fork candidates**: EIP-7907 (meter and increase contract code size, candidate)
- **Manual review required**: Yes

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/Checkpoints.sol:177`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
175:         uint256 high
176:     ) private view returns (uint256) {
177:         while (low < high) {
178:             uint256 mid = Math.average(low, high);
179:             if (_unsafeAccess(self, mid)._key > key) {
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/Checkpoints.sol:201`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
199:         uint256 high
200:     ) private view returns (uint256) {
201:         while (low < high) {
202:             uint256 mid = Math.average(low, high);
203:             if (_unsafeAccess(self, mid)._key < key) {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/Checkpoints.sol:219`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
217:         uint256 pos
218:     ) private pure returns (Checkpoint256 storage result) {
219:         assembly {
220:             mstore(0x00, self.slot)
221:             result.slot := add(keccak256(0x00, 0x20), mul(pos, 2))
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/Checkpoints.sol:380`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
378:         uint256 high
379:     ) private view returns (uint256) {
380:         while (low < high) {
381:             uint256 mid = Math.average(low, high);
382:             if (_unsafeAccess(self, mid)._key > key) {
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/Checkpoints.sol:404`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
402:         uint256 high
403:     ) private view returns (uint256) {
404:         while (low < high) {
405:             uint256 mid = Math.average(low, high);
406:             if (_unsafeAccess(self, mid)._key < key) {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/Checkpoints.sol:422`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
420:         uint256 pos
421:     ) private pure returns (Checkpoint224 storage result) {
422:         assembly {
423:             mstore(0x00, self.slot)
424:             result.slot := add(keccak256(0x00, 0x20), pos)
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/Checkpoints.sol:583`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
581:         uint256 high
582:     ) private view returns (uint256) {
583:         while (low < high) {
584:             uint256 mid = Math.average(low, high);
585:             if (_unsafeAccess(self, mid)._key > key) {
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/Checkpoints.sol:607`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
605:         uint256 high
606:     ) private view returns (uint256) {
607:         while (low < high) {
608:             uint256 mid = Math.average(low, high);
609:             if (_unsafeAccess(self, mid)._key < key) {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/Checkpoints.sol:625`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
623:         uint256 pos
624:     ) private pure returns (Checkpoint208 storage result) {
625:         assembly {
626:             mstore(0x00, self.slot)
627:             result.slot := add(keccak256(0x00, 0x20), pos)
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/Checkpoints.sol:786`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
784:         uint256 high
785:     ) private view returns (uint256) {
786:         while (low < high) {
787:             uint256 mid = Math.average(low, high);
788:             if (_unsafeAccess(self, mid)._key > key) {
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/Checkpoints.sol:810`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
808:         uint256 high
809:     ) private view returns (uint256) {
810:         while (low < high) {
811:             uint256 mid = Math.average(low, high);
812:             if (_unsafeAccess(self, mid)._key < key) {
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/Checkpoints.sol:828`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
826:         uint256 pos
827:     ) private pure returns (Checkpoint160 storage result) {
828:         assembly {
829:             mstore(0x00, self.slot)
830:             result.slot := add(keccak256(0x00, 0x20), pos)
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/CircularBuffer.sol:145`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
143:         uint256 modulus = self._data.length;
144:         uint256 total = Math.min(index, modulus); // count(self)
145:         for (uint256 i = 0; i < total; ++i) {
146:             if (Arrays.unsafeAccess(self._data, (index - i - 1) % modulus).value == value) {
147:                 return true;
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `utils/structs/EnumerableMap.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Rule confidence**: low
- **Rule rationale**: File size is a rough proxy for deployed bytecode size. A raised max contract size would relax rather than break constraints, so this is a watch point only.
- **Related fork candidates**: EIP-7907 (meter and increase contract code size, candidate)
- **Manual review required**: Yes

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/EnumerableMap.sol:104`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
102:     function clear(Bytes32ToBytes32Map storage map) internal {
103:         uint256 len = length(map);
104:         for (uint256 i = 0; i < len; ++i) {
105:             delete map._values[map._keys.at(i)];
106:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:292`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
290:         uint256[] memory result;
291: 
292:         assembly ("memory-safe") {
293:             result := store
294:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:311`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
309:         uint256[] memory result;
310: 
311:         assembly ("memory-safe") {
312:             result := store
313:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:415`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
413:         uint256[] memory result;
414: 
415:         assembly ("memory-safe") {
416:             result := store
417:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:434`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
432:         uint256[] memory result;
433: 
434:         assembly ("memory-safe") {
435:             result := store
436:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:538`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
536:         uint256[] memory result;
537: 
538:         assembly ("memory-safe") {
539:             result := store
540:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:557`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
555:         uint256[] memory result;
556: 
557:         assembly ("memory-safe") {
558:             result := store
559:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:661`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
659:         address[] memory result;
660: 
661:         assembly ("memory-safe") {
662:             result := store
663:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:680`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
678:         address[] memory result;
679: 
680:         assembly ("memory-safe") {
681:             result := store
682:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:784`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
782:         address[] memory result;
783: 
784:         assembly ("memory-safe") {
785:             result := store
786:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:807`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
805:         address[] memory result;
806: 
807:         assembly ("memory-safe") {
808:             result := store
809:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:911`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
909:         address[] memory result;
910: 
911:         assembly ("memory-safe") {
912:             result := store
913:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:934`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
932:         address[] memory result;
933: 
934:         assembly ("memory-safe") {
935:             result := store
936:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:1038`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1036:         bytes32[] memory result;
1037: 
1038:         assembly ("memory-safe") {
1039:             result := store
1040:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:1057`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1055:         bytes32[] memory result;
1056: 
1057:         assembly ("memory-safe") {
1058:             result := store
1059:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:1161`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1159:         bytes32[] memory result;
1160: 
1161:         assembly ("memory-safe") {
1162:             result := store
1163:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:1184`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1182:         bytes32[] memory result;
1183: 
1184:         assembly ("memory-safe") {
1185:             result := store
1186:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:1288`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1286:         bytes4[] memory result;
1287: 
1288:         assembly ("memory-safe") {
1289:             result := store
1290:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableMap.sol:1307`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1305:         bytes4[] memory result;
1306: 
1307:         assembly ("memory-safe") {
1308:             result := store
1309:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/EnumerableMap.sol:1355`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
1353:     function clear(BytesToBytesMap storage map) internal {
1354:         uint256 len = length(map);
1355:         for (uint256 i = 0; i < len; ++i) {
1356:             delete map._values[map._keys.at(i)];
1357:         }
```

### [Informational] glamsterdam-contract-size-watch

- **Location**: `utils/structs/EnumerableSet.sol:1`
- **Review note**: Large Solidity source file. Review contract-size assumptions against Glamsterdam max contract size discussions.
- **Rule confidence**: low
- **Rule rationale**: File size is a rough proxy for deployed bytecode size. A raised max contract size would relax rather than break constraints, so this is a watch point only.
- **Related fork candidates**: EIP-7907 (meter and increase contract code size, candidate)
- **Manual review required**: Yes

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/EnumerableSet.sol:136`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
134:     function _clear(Set storage set) private {
135:         uint256 len = _length(set);
136:         for (uint256 i = 0; i < len; ++i) {
137:             delete set._positions[set._values[i]];
138:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/EnumerableSet.sol:197`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
195:             uint256 len = end - start;
196:             bytes32[] memory result = new bytes32[](len);
197:             for (uint256 i = 0; i < len; ++i) {
198:                 result[i] = Arrays.unsafeAccess(set._values, start + i).value;
199:             }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableSet.sol:280`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
278:         bytes32[] memory result;
279: 
280:         assembly ("memory-safe") {
281:             result := store
282:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableSet.sol:299`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
297:         bytes32[] memory result;
298: 
299:         assembly ("memory-safe") {
300:             result := store
301:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableSet.sol:382`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
380:         bytes4[] memory result;
381: 
382:         assembly ("memory-safe") {
383:             result := store
384:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableSet.sol:401`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
399:         bytes4[] memory result;
400: 
401:         assembly ("memory-safe") {
402:             result := store
403:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableSet.sol:484`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
482:         address[] memory result;
483: 
484:         assembly ("memory-safe") {
485:             result := store
486:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableSet.sol:503`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
501:         address[] memory result;
502: 
503:         assembly ("memory-safe") {
504:             result := store
505:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableSet.sol:586`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
584:         uint256[] memory result;
585: 
586:         assembly ("memory-safe") {
587:             result := store
588:         }
```

### [Informational] glamsterdam-low-level-evm

- **Location**: `utils/structs/EnumerableSet.sol:605`
- **Review note**: Low-level EVM usage. Review low-level EVM assumptions against proposed opcode and EVM behavior changes.
- **Rule confidence**: low
- **Rule rationale**: Assembly blocks and low-level calls may rely on opcode gas costs or semantics, but most uses are routine library plumbing. The rule flags surface area for review, not concrete incompatibilities.
- **Related fork candidates**: New EVM opcodes (candidates), Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
603:         uint256[] memory result;
604: 
605:         assembly ("memory-safe") {
606:             result := store
607:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/EnumerableSet.sol:686`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
684:     function clear(StringSet storage set) internal {
685:         uint256 len = length(set);
686:         for (uint256 i = 0; i < len; ++i) {
687:             delete set._positions[set._values[i]];
688:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/EnumerableSet.sol:747`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
745:             uint256 len = end - start;
746:             string[] memory result = new string[](len);
747:             for (uint256 i = 0; i < len; ++i) {
748:                 result[i] = Arrays.unsafeAccess(set._values, start + i).value;
749:             }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/EnumerableSet.sol:828`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
826:     function clear(BytesSet storage set) internal {
827:         uint256 len = length(set);
828:         for (uint256 i = 0; i < len; ++i) {
829:             delete set._positions[set._values[i]];
830:         }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/EnumerableSet.sol:889`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
887:             uint256 len = end - start;
888:             bytes[] memory result = new bytes[](len);
889:             for (uint256 i = 0; i < len; ++i) {
890:                 result[i] = Arrays.unsafeAccess(set._values, start + i).value;
891:             }
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/Heap.sol:250`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
248:     ) private {
249:         unchecked {
250:             while (index > 0) {
251:                 uint256 parentIndex = (index - 1) / 2;
252:                 uint256 parentValue = self.tree.unsafeAccess(parentIndex).value;
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/MerkleTree.sol:98`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
96:         // Build each root of zero-filled subtrees
97:         bytes32 currentZero = zero;
98:         for (uint256 i = 0; i < treeDepth; ++i) {
99:             Arrays.unsafeAccess(self._zeros, i).value = currentZero;
100:             currentZero = fnHash(currentZero, currentZero);
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/MerkleTree.sol:153`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
151:         uint256 currentIndex = index;
152:         bytes32 currentLevelHash = leaf;
153:         for (uint256 i = 0; i < treeDepth; i++) {
154:             // Reaching the parent node, is currentLevelHash the left child?
155:             bool isLeft = currentIndex % 2 == 0;
```

### [Informational] glamsterdam-gas-sensitive-loop

- **Location**: `utils/structs/MerkleTree.sol:235`
- **Review note**: Gas-sensitive loop. Review loop bounds and gas sensitivity against Glamsterdam gas repricing proposals.
- **Rule confidence**: low
- **Rule rationale**: A loop is only gas-sensitive when its bound is dynamic or its body performs repriced operations. Keyword matching cannot see bounds, so this rule is deliberately high-recall and most matches need quick dismissal rather than action.
- **Related fork candidates**: Glamsterdam gas repricing package (candidate)
- **Manual review required**: Yes

```solidity
233:             bytes32 currentLevelHashOld = oldValue;
234:             bytes32 currentLevelHashNew = newValue;
235:             for (uint32 i = 0; i < treeDepth; i++) {
236:                 bool isLeft = currentIndex % 2 == 0;
237: 
```

### [Informational] glamsterdam-block-context

- **Location**: `utils/types/Time.sol:27`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
25:      */
26:     function timestamp() internal view returns (uint48) {
27:         return SafeCast.toUint48(block.timestamp);
28:     }
29: 
```

### [Informational] glamsterdam-block-context

- **Location**: `utils/types/Time.sol:34`
- **Review note**: Block context dependency. Review block context assumptions as Glamsterdam candidates include protocol-level changes such as ePBS and Block-Level Access Lists.
- **Rule confidence**: medium
- **Rule rationale**: Block-context values are produced by the proposer/builder pipeline. ePBS and Block-Level Access Lists change who assembles blocks and when state access is committed, so timing or ordering assumptions deserve a second look.
- **Related fork candidates**: EIP-7732 (ePBS, candidate), EIP-7928 (Block-Level Access Lists, candidate)
- **Manual review required**: Yes

```solidity
32:      */
33:     function blockNumber() internal view returns (uint48) {
34:         return SafeCast.toUint48(block.number);
35:     }
36: 
```

## Tuning and suppression

Reviewed-and-accepted matches can be suppressed so repeat runs stay focused:

- Inline: append `// glamsterdam-ignore` to the flagged line, or `// glamsterdam-ignore: <detector>[, <detector>]` to suppress specific rules.
- Baseline: add a `glamsterdam-baseline.json` file at the scan root with `{"suppressions": [{"detector": "...", "file": "...", "line": 12}]}`. Omitted keys act as wildcards.

## Limitations

- Glamsterdam EIPs are still under consideration and may change; see EIP-7773 and forkcast.org for current status.
- Readiness heuristics are separate from Slither static-analysis evidence.
- Findings are review prompts, not vulnerability claims.
- Low-confidence rules trade precision for recall by design; use suppression to record triage decisions.