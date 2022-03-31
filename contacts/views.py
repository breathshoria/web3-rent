import json
from web3 import Web3
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from .models import Contact
from listings.models import Contract, Listing
from .forms import ContactForm


def accept_mail(listing_id, contact_id):
    list = Listing.objects.get(id=listing_id)
    new_contact = Contact.objects.get(id=contact_id)
    subject = 'Совершена новая сделка'
    message = 'Здравствуйте,' + '\n\n' + 'ваша квартира' + ' ' + '(' + str(
        list.title) + ')' + '\n' + 'в итоге заключения смарт-контракта:' + ' ' + 'https://kovan.etherscan.io/address/' + str(
        list.contract.sc_address) + ' ' + 'получила арендующего' + '\n\n' + 'Почта арендующего:' + ': ' + str(
        new_contact.user.email) + '\n' + 'Сообщение:' + ' ' + str(
        new_contact.message) + '\n' + 'С уважением,' + '\n' + 'команда CryptRent' + '\n' + 'cryprent24.com'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [list.user.email, ]
    send_mail(subject, message, email_from, recipient_list)
    return print('Email about new contact')


def get_contact(request, listing):
    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            property = Listing.objects.get(id=listing)
            kovan_url = 'https://kovan.infura.io/v3/050656a9183d4fd7bcac660f237a1724'
            web3 = Web3(Web3.HTTPProvider(kovan_url))
            web3.eth.defaultAccount = Web3.toChecksumAddress(request.user.eth_acc)
            abi = json.loads(
                '[{"constant":false,"inputs":[],"name":"TerminateContract","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getHouse","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTenant","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"rentsPaid","outputs":[{"name":"month","type":"uint256"},{"name":"amount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTermLength","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"status","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"securityDeposit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_myid","type":"bytes32"},{"name":"_result","type":"string"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"renter","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_myid","type":"bytes32"},{"name":"_result","type":"string"},{"name":"_proof","type":"bytes"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"lateFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getStatus","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"CheckTerms","outputs":[{"name":"","type":"bytes32"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getSecurityDeposit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"myid","type":"bytes32"},{"name":"result","type":"bool"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"termLength","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getRenter","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"rent","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"payRent","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"tenant","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTimeCreated","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"tokenFallback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"beginLease","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getRent","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"timeCreated","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"house","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_rent","type":"uint256"},{"name":"_house","type":"string"},{"name":"_termLength","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":false,"stateMutability":"nonpayable","type":"fallback"},{"anonymous":false,"inputs":[],"name":"rentPaid","type":"event"},{"anonymous":false,"inputs":[],"name":"contractActive","type":"event"},{"anonymous":false,"inputs":[],"name":"contractTerminated","type":"event"},{"anonymous":false,"inputs":[],"name":"termBreached","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"description","type":"string"}],"name":"LogNewOraclizeQuery","type":"event"}]')
            private_key = form.cleaned_data['private_key']
            acct = web3.eth.account.privateKeyToAccount(private_key)
            address = Web3.toChecksumAddress(property.contract.sc_address)
            contract = web3.eth.contract(
                address=address,
                abi=abi
            )
            tx_hash = contract.functions.beginLease().buildTransaction(
                {'from': acct.address, 'value': web3.toWei(1000000, 'wei'),
                 'nonce': web3.eth.getTransactionCount(acct.address), })
            signed = acct.signTransaction(tx_hash)
            tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            print(tx_receipt)
            contact = Contact.objects.create()
            contact.listing = property
            contact.contract = property.contract
            contact.message = form.cleaned_data['message']
            contact.user = request.user
            contact.save()
            accept_mail(property.id, contact.id)
            property.contract.tenant = request.user.eth_acc
            property.contract.save()
            return redirect('dashboard')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()
    return redirect('dashboard')
