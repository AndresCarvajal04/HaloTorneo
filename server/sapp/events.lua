-- SAPP Lua Script con soporte de Timer continuo y Votaciones Personalizadas
api_version = "1.12.0.0"

local command_file = "command_queue.txt"
local voting_active = false
local vote_counts = {}
local player_voted = {}
local current_vote_pool = {}

function CheckWebCommandBridge()
    local f = io.open(command_file, "r")
    if f then
        local content = f:read("*a")
        f:close()
        os.remove(command_file)

        if content and content ~= "" then
            for line in string.gmatch(content, "[^\r\n]+") do
                line = line:match("^%s*(.-)%s*$")
                if line ~= "" then
                    if line:sub(1, 14) == "set_vote_pool " then
                        StartCustomVote(line:sub(15))
                    elseif line == "endvote" then
                        EndCustomVote()
                    else
                        print("[SAPP-BRIDGE] Ejecutando: " .. line)
                        execute_command(line)
                    end
                end
            end
        end
    end
    return true
end

function StartCustomVote(pool_str)
    voting_active = true
    vote_counts = {}
    player_voted = {}
    current_vote_pool = {}

    local idx = 1
    for map_name in string.gmatch(pool_str, "([^,]+)") do
        map_name = map_name:match("^%s*(.-)%s*$")
        if map_name ~= "" then
            table.insert(current_vote_pool, map_name)
            vote_counts[idx] = 0
            idx = idx + 1
        end
    end

    execute_command("say * [VOTACION] Vota por el siguiente mapa (1, 2, 3...):")
    for i, m in ipairs(current_vote_pool) do
        execute_command("say * [" .. i .. "] " .. m)
    end
end

function EndCustomVote()
    if not voting_active then return end
    voting_active = false

    local best_idx = 1
    local highest_votes = -1
    for i = 1, #current_vote_pool do
        local count = vote_counts[i] or 0
        if count > highest_votes then
            highest_votes = count
            best_idx = i
        end
    end

    local winner = current_vote_pool[best_idx]
    if winner then
        execute_command("say * [VOTACION] Ganador: " .. winner .. " con " .. highest_votes .. " votos!")
        execute_command("sv_map " .. winner .. " team_slayer")
    end
end

function OnChat(PlayerIndex, Message, Type)
    if voting_active then
        local choice = tonumber(Message)
        if choice and choice >= 1 and choice <= #current_vote_pool then
            if player_voted[PlayerIndex] then
                execute_command("rprint " .. PlayerIndex .. " Ya has votado en esta ronda!")
            else
                player_voted[PlayerIndex] = true
                vote_counts[choice] = (vote_counts[choice] or 0) + 1
                execute_command("rprint " .. PlayerIndex .. " Voto registrado por [" .. choice .. "]!")
            end
            return false
        end
    end
    return true
end

function OnCommand(PlayerIndex, Command, Environment, Password)
    local cmd = Command:lower()
    if cmd == "endvote" then
        EndCustomVote()
        return false
    end
    return true
end

function OnScriptLoad()
    register_callback(cb['EVENT_COMMAND'], "OnCommand")
    register_callback(cb['EVENT_CHAT'], "OnChat")
    timer(300, "CheckWebCommandBridge")
    print("[TOURNAMENT] SAPP Lua Command Bridge Inicializado Correctamente.")
end
