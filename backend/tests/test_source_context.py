from app.models.schemas import Finding, Severity
from app.services.source_context import attach_source_context


def test_attach_source_context_extracts_function(tmp_path):
    source = tmp_path / "Vault.sol"
    source.write_text(
        "\n".join(
            [
                "pragma solidity ^0.8.20;",
                "contract Vault {",
                "    mapping(address => uint256) public balances;",
                "    function withdraw() external {",
                "        uint256 amount = balances[msg.sender];",
                "        (bool ok,) = msg.sender.call{value: amount}(\"\");",
                "        require(ok);",
                "        balances[msg.sender] = 0;",
                "    }",
                "}",
            ]
        ),
        encoding="utf-8",
    )
    finding = Finding(
        id="finding-1",
        detector="reentrancy-eth",
        severity=Severity.HIGH,
        description="Reentrancy in withdraw",
        file="Vault.sol",
        line=6,
    )

    attach_source_context([finding], tmp_path)

    assert finding.source_context is not None
    assert "function withdraw" in finding.source_context
    assert "msg.sender.call" in finding.source_context
    assert finding.source_start_line == 4
    assert finding.source_end_line == 9
