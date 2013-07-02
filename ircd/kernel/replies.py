replies = {
    'RPL_WELCOME': ('001', 'Welcome to the Internet Relay Network'),
    'RPL_MYINFO': ('004', 'ircd 0.1 i ov'),
    'RPL_ISUPPORT': ('005', 'PREFIX=(qov).@+ CHANTYPES=# CHARSET=UTF-8 ' +
                            ':are supported by this server'),

    'RPL_ENDOFWHO': ('315', '%s :End of /WHO list'),
    'RPL_CHANNELMODEIS': ('324', '%s +%s'),
    'RPL_NOTOPIC': ('331', '%s :No topic is set'),
    'RPL_TOPIC': ('332', '%s :%s'),
    'RPL_WHOREPLY': ('352', '%s %s %s %s %s %s%s :%s %s'),
    'RPL_NAMREPLY': ('353', '= %s :%s'),
    'RPL_ENDOFNAMES': ('366', '%s :End of NAMES list'),
    'RPL_ENDOFBANLIST': ('368', '%s :End of Channel Ban List'),

    'ERR_NOSUCHNICK': ('401', '%s :No such nick'),
    'ERR_NOSUCHCHANNEL': ('403', '%s :No such channel'),
    'ERR_CANNOTSENDTOCHAN': ('404', '%s :Cannot send to channel'),
    'ERR_UNKNOWNCOMMAND': ('421', '%s :Unknown command'),
    'ERR_ERRONEOUSNICKNAME': ('432', '%s :Erroneous nickname'),
    'ERR_USERNOTINCHANNEL': ('441', '%s %s :They aren\'t on that channel'),
    'ERR_NOTONCHANNEL': ('442', '%s :You\'re not on that channel'),
    'ERR_NOTREGISTERED': ('451', ':You have not registered'),
    'ERR_NEEDMOREPARAMS': ('461', '%s :Not enough parameters'),
    'ERR_ALREADYREGISTRED': ('462', ':Already registered'),
    'ERR_UNKNOWNMODE': ('472', '%s :is an unknown mode char to me'),
    'ERR_BADCHANNAME': ('479', '%s :Illegal channel name'),
    'ERR_CHANOPRIVSNEEDED': ('482', '%s :You\'re not channel operator'),

    'RPL_ACCESSADD': ('801', '%s %s %s %s %s :%s'),
    'RPL_ACCESSDELETE': ('802', '%s %s %s'),
    'RPL_ACCESSSTART': ('803', '%s :Start of access entries'),
    'RPL_ACCESSLIST': ('804', '%s %s %s %s %s :%s'),
    'RPL_ACCESSEND': ('805', '%s :End of access entries'),

    'ERR_AUTHENTICATIONFAILED': ('910', ':Authentication failed (%s)'),
    'ERR_ALREADYONCHANNEL': ('927', '%s :Already in the channel'),

    'ERR_ERRONEOUSUSERNAME': ('997', '%s :Erroneous username'),
    'ERR_NONUTF8': ('998', ':Non UTF-8 message'),
}
