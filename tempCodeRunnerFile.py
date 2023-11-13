for i, time_threshold in enumerate(ENEMY_SPAWN_RATE):
                 if gameSeconds >= time_threshold:
                     if ENEMY_TYPES[i] not in current_enemy_types:
                         current_enemy_types.append(ENEMY_TYPES[i])