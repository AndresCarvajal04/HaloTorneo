api_version = "1.12.0.0"

function OnScriptLoad()
    register_callback(cb.EVENT_JOIN, "OnPlayerJoin")
end

function OnScriptUnload()

end

function OnPlayerJoin(playerIndex)
	print("sample_script.lua -> Hello, ", get_var(playerIndex, "$name"))
end