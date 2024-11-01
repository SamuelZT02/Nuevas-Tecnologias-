//Samuel Jabes Zapata Torres 1914266
//NT grupo:066
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract contrato{
    struct Usuario {
        string nombre;
        string saludo;
    }

    mapping (address => Usuario) public usuarios;

    function guardarNombre(string memory _nombre) public {
        usuarios[msg.sender].nombre = _nombre;
    }
    function saludar() public view returns (string memory) {
        string memory nombreUsuario = usuarios[msg.sender].nombre;
        return string(abi.encodePacked("Hola, ", nombreUsuario, "!"));
    }

}