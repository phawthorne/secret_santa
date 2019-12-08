from secret_santa import assigner, mailer, logger


def main():
    emails = {}
    with open('data/participants.txt') as f:
        for l in f:
            name, email = l.strip().split(',')
            emails[name] = email
    names = sorted(emails.keys())
    print(names)

    excluded_sets = []
    with open('data/excluded_sets.txt') as f:
        for l in f:
            excluded_sets.append(l.strip().split(','))

    private_data = {}
    with open('data/privatedata.txt') as f:
        for l in f:
            key, value = l.strip().split(',')
            private_data[key.strip()] = value.strip()

    past_exchanges = []
    with open('log/log.csv') as f:
        f.readline()
        for l in f:
            year, giver, recipient = l.strip().split(',')
            past_exchanges.append((giver, recipient))

    assignment = assigner.generate_assignment(names, excluded_sets,
                                              excluded_assignments=past_exchanges)
    logger.log(assignment, 'log/log.txt')
    mailer.send_mails(assignment, emails, private_data, for_real=True)


if __name__ == '__main__':
    main()
