https://github.com/ajanata/PretendYoureXyzzy/blob/ed08e371978529db8a908e266dc1a8add1d37967/./src/main/java/net/socialgamer/cah/data/Game.java#L221-L255
```
🈚️

Mock util validated the number of `User.joinGame` calls.

java.lang.AssertionError: 
  Expectation failure on verify:
    User.joinGame(<any>): expected: 3, actual: 0
```
```
//@ ensures players.size() == \old(players.size()) + 1;
//@ ensures getPlayerForUser(user) != null;
//@ ensures players.get(players.size() - 1).getUser() == user;
//@ ensures getPlayerForUser(user) == players.get(players.size() - 1);
//@ ensures (\old(host) == null) ==> host == getPlayerForUser(user);
//@ ensures (\old(host) != null) ==> host == \old(host);
```
[0, 9, 10, 11, 12]
===== 0 =====
```
                 throw new TooManyPlayersException();
             }
             // this will throw IllegalStateException if the user is already in a game, including this one.
-            user.joinGame(this);
+            
             final Player player = new Player(user);
             players.add(player);
             if (host == null) {
```
```
    /**
     * Add a player to the game.
     *
     * Synchronizes on {@link #players}.
     *
     * @param user
     *          Player to add to this game.
     * @throws TooManyPlayersException
     *           Thrown if this game is at its maximum player capacity.
     * @throws IllegalStateException
     *           Thrown if {@code user} is already in a game.
     */
    public void addPlayer(final User user) throws TooManyPlayersException, IllegalStateException {
        logger.info(String.format("%s joined game %d.", user.toString(), id));
        synchronized (players) {
            if (options.playerLimit >= 3 && players.size() >= options.playerLimit) {
                throw new TooManyPlayersException();
            }
            // this will throw IllegalStateException if the user is already in a game, including this one.
            
            final Player player = new Player(user);
            players.add(player);
            if (host == null) {
                host = player;
            }
        }

        final HashMap<ReturnableData, Object> data = getEventMap();
        data.put(LongPollResponse.EVENT, LongPollEvent.GAME_PLAYER_JOIN.toString());
        data.put(LongPollResponse.NICKNAME, user.getNickname());
        broadcastToPlayers(MessageType.GAME_PLAYER_EVENT, data);

        // Don't do this anymore, it was driving up a crazy amount of traffic.
        // gameManager.broadcastGameListRefresh();
    }
```
===== 9 =====
```
 
         final HashMap<ReturnableData, Object> data = getEventMap();
         data.put(LongPollResponse.EVENT, LongPollEvent.GAME_PLAYER_JOIN.toString());
-        data.put(LongPollResponse.NICKNAME, user.getNickname());
+        
         broadcastToPlayers(MessageType.GAME_PLAYER_EVENT, data);
 
         // Don't do this anymore, it was driving up a crazy amount of traffic.
```
```
    /**
     * Add a player to the game.
     *
     * Synchronizes on {@link #players}.
     *
     * @param user
     *          Player to add to this game.
     * @throws TooManyPlayersException
     *           Thrown if this game is at its maximum player capacity.
     * @throws IllegalStateException
     *           Thrown if {@code user} is already in a game.
     */
    public void addPlayer(final User user) throws TooManyPlayersException, IllegalStateException {
        logger.info(String.format("%s joined game %d.", user.toString(), id));
        synchronized (players) {
            if (options.playerLimit >= 3 && players.size() >= options.playerLimit) {
                throw new TooManyPlayersException();
            }
            // this will throw IllegalStateException if the user is already in a game, including this one.
            user.joinGame(this);
            final Player player = new Player(user);
            players.add(player);
            if (host == null) {
                host = player;
            }
        }

        final HashMap<ReturnableData, Object> data = getEventMap();
        data.put(LongPollResponse.EVENT, LongPollEvent.GAME_PLAYER_JOIN.toString());
        
        broadcastToPlayers(MessageType.GAME_PLAYER_EVENT, data);

        // Don't do this anymore, it was driving up a crazy amount of traffic.
        // gameManager.broadcastGameListRefresh();
    }
```
===== 10 =====
```
 
         final HashMap<ReturnableData, Object> data = getEventMap();
         data.put(LongPollResponse.EVENT, LongPollEvent.GAME_PLAYER_JOIN.toString());
-        data.put(LongPollResponse.NICKNAME, user.getNickname());
+        data.put(LongPollResponse.NICKNAME, ""); // Sets nickname to an empty string
         broadcastToPlayers(MessageType.GAME_PLAYER_EVENT, data);
 
         // Don't do this anymore, it was driving up a crazy amount of traffic.
```
```
    /**
     * Add a player to the game.
     *
     * Synchronizes on {@link #players}.
     *
     * @param user
     *          Player to add to this game.
     * @throws TooManyPlayersException
     *           Thrown if this game is at its maximum player capacity.
     * @throws IllegalStateException
     *           Thrown if {@code user} is already in a game.
     */
    public void addPlayer(final User user) throws TooManyPlayersException, IllegalStateException {
        logger.info(String.format("%s joined game %d.", user.toString(), id));
        synchronized (players) {
            if (options.playerLimit >= 3 && players.size() >= options.playerLimit) {
                throw new TooManyPlayersException();
            }
            // this will throw IllegalStateException if the user is already in a game, including this one.
            user.joinGame(this);
            final Player player = new Player(user);
            players.add(player);
            if (host == null) {
                host = player;
            }
        }

        final HashMap<ReturnableData, Object> data = getEventMap();
        data.put(LongPollResponse.EVENT, LongPollEvent.GAME_PLAYER_JOIN.toString());
        data.put(LongPollResponse.NICKNAME, ""); // Sets nickname to an empty string
        broadcastToPlayers(MessageType.GAME_PLAYER_EVENT, data);

        // Don't do this anymore, it was driving up a crazy amount of traffic.
        // gameManager.broadcastGameListRefresh();
    }
```
===== 11 =====
```
 
         final HashMap<ReturnableData, Object> data = getEventMap();
         data.put(LongPollResponse.EVENT, LongPollEvent.GAME_PLAYER_JOIN.toString());
-        data.put(LongPollResponse.NICKNAME, user.getNickname());
+        data.put(LongPollResponse.NICKNAME, null);
         broadcastToPlayers(MessageType.GAME_PLAYER_EVENT, data);
 
         // Don't do this anymore, it was driving up a crazy amount of traffic.
```
```
    /**
     * Add a player to the game.
     *
     * Synchronizes on {@link #players}.
     *
     * @param user
     *          Player to add to this game.
     * @throws TooManyPlayersException
     *           Thrown if this game is at its maximum player capacity.
     * @throws IllegalStateException
     *           Thrown if {@code user} is already in a game.
     */
    public void addPlayer(final User user) throws TooManyPlayersException, IllegalStateException {
        logger.info(String.format("%s joined game %d.", user.toString(), id));
        synchronized (players) {
            if (options.playerLimit >= 3 && players.size() >= options.playerLimit) {
                throw new TooManyPlayersException();
            }
            // this will throw IllegalStateException if the user is already in a game, including this one.
            user.joinGame(this);
            final Player player = new Player(user);
            players.add(player);
            if (host == null) {
                host = player;
            }
        }

        final HashMap<ReturnableData, Object> data = getEventMap();
        data.put(LongPollResponse.EVENT, LongPollEvent.GAME_PLAYER_JOIN.toString());
        data.put(LongPollResponse.NICKNAME, null);
        broadcastToPlayers(MessageType.GAME_PLAYER_EVENT, data);

        // Don't do this anymore, it was driving up a crazy amount of traffic.
        // gameManager.broadcastGameListRefresh();
    }
```
===== 12 =====
```
         final HashMap<ReturnableData, Object> data = getEventMap();
         data.put(LongPollResponse.EVENT, LongPollEvent.GAME_PLAYER_JOIN.toString());
         data.put(LongPollResponse.NICKNAME, user.getNickname());
-        broadcastToPlayers(MessageType.GAME_PLAYER_EVENT, data);
+        
 
         // Don't do this anymore, it was driving up a crazy amount of traffic.
         // gameManager.broadcastGameListRefresh();
```
```
    /**
     * Add a player to the game.
     *
     * Synchronizes on {@link #players}.
     *
     * @param user
     *          Player to add to this game.
     * @throws TooManyPlayersException
     *           Thrown if this game is at its maximum player capacity.
     * @throws IllegalStateException
     *           Thrown if {@code user} is already in a game.
     */
    public void addPlayer(final User user) throws TooManyPlayersException, IllegalStateException {
        logger.info(String.format("%s joined game %d.", user.toString(), id));
        synchronized (players) {
            if (options.playerLimit >= 3 && players.size() >= options.playerLimit) {
                throw new TooManyPlayersException();
            }
            // this will throw IllegalStateException if the user is already in a game, including this one.
            user.joinGame(this);
            final Player player = new Player(user);
            players.add(player);
            if (host == null) {
                host = player;
            }
        }

        final HashMap<ReturnableData, Object> data = getEventMap();
        data.put(LongPollResponse.EVENT, LongPollEvent.GAME_PLAYER_JOIN.toString());
        data.put(LongPollResponse.NICKNAME, user.getNickname());
        

        // Don't do this anymore, it was driving up a crazy amount of traffic.
        // gameManager.broadcastGameListRefresh();
    }
```
