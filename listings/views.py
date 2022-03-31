import json
import locale
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from web3 import Web3
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from django.views.generic.edit import FormView
from .models import Listing, Contract, User
from contacts.models import Contact
from .forms import NewListingForm, DeployingForm, PayForm, TerminationForm


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)


    context = {
        'listings': paged_listings
    }

    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    price_eth = round(listing.price/11503, 5)
    context = {
        'listing': listing, 'price_eth' :price_eth,
    }

    return render(request, 'listings/listing.html', context)

def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
      keywords = request.GET['keywords']
      if keywords:
        queryset_list = queryset_list.filter(description__icontains=keywords)  

    # City
    if 'city' in request.GET:
      city = request.GET['city']
      if city:
        queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if 'state' in request.GET:
      state = request.GET['state']
      if state:
        queryset_list = queryset_list.filter(state__iexact=state) 

    # Bedrooms
    if 'bedrooms' in request.GET:
      bedrooms = request.GET['bedrooms']
      if bedrooms:
        queryset_list = queryset_list.filter(bedrooms__iexact=bedrooms)

    # Price
    if 'price' in request.GET:
      price = request.GET['price']
      if price:
        queryset_list = queryset_list.filter(price__lte=price)


    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)


class NewListingView(FormView):
    template_name = 'listings/add_listing.html'
    form_class = NewListingForm
    id = None

    def get_success_url(self):
        return reverse_lazy('listing', args = (self.id,))

    def form_valid(self, form):
        print(self.request)
        form.instance.user = self.request.user
        object = form.save()
        self.id = object.id
        return super().form_valid(form)



def delete(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    print(listing)
    listing.delete()



    return redirect('dashboard')


def delete_contact(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    contact.delete()


    return redirect('dashboard')


def get_deploying(request, listing_id):
    # if this is a POST request we need to process the form data



    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DeployingForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            object = Listing.objects.get(id=listing_id)
            kovan_url = 'https://kovan.infura.io/v3/050656a9183d4fd7bcac660f237a1724'
            web3 = Web3(Web3.HTTPProvider(kovan_url))
            print(request.user.eth_acc)
            web3.eth.defaultAccount = Web3.toChecksumAddress(request.user.eth_acc)

            abi = json.loads('[{"constant":false,"inputs":[],"name":"TerminateContract","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getHouse","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTenant","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"rentsPaid","outputs":[{"name":"month","type":"uint256"},{"name":"amount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTermLength","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"status","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"securityDeposit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_myid","type":"bytes32"},{"name":"_result","type":"string"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"renter","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_myid","type":"bytes32"},{"name":"_result","type":"string"},{"name":"_proof","type":"bytes"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"lateFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getStatus","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"CheckTerms","outputs":[{"name":"","type":"bytes32"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getSecurityDeposit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"myid","type":"bytes32"},{"name":"result","type":"bool"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"termLength","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getRenter","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"rent","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"payRent","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"tenant","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTimeCreated","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"tokenFallback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"beginLease","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getRent","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"timeCreated","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"house","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_rent","type":"uint256"},{"name":"_house","type":"string"},{"name":"_termLength","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":false,"stateMutability":"nonpayable","type":"fallback"},{"anonymous":false,"inputs":[],"name":"rentPaid","type":"event"},{"anonymous":false,"inputs":[],"name":"contractActive","type":"event"},{"anonymous":false,"inputs":[],"name":"contractTerminated","type":"event"},{"anonymous":false,"inputs":[],"name":"termBreached","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"description","type":"string"}],"name":"LogNewOraclizeQuery","type":"event"}]')
            bytecode = '6080604052620f4240600c55620f4240600d553480156200001f57600080fd5b506040516200293238038062002932833981018060405260608110156200004557600080fd5b810190808051906020019092919080516401000000008111156200006857600080fd5b828101905060208101848111156200007f57600080fd5b81518560018202830111640100000000821117156200009d57600080fd5b50509291906020018051906020019092919050505033600660016101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555082600c8190555081600890805190602001906200011292919062000145565b5080600b8190555042600a819055506000600f60006101000a81548160ff021916908315150217905550505050620001f4565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f106200018857805160ff1916838001178555620001b9565b82800160010185558215620001b9579182015b82811115620001b85782518255916020019190600101906200019b565b5b509050620001c89190620001cc565b5090565b620001f191905b80821115620001ed576000816000905550600101620001d3565b5090565b90565b61272e80620002046000396000f3fe608060405260043610610154576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063028cb2081461016b57806304e2064f146101755780630b3bb02414610205578063165991291461025c5780631cb21db5146102b2578063200d2ed2146102dd578063220e5ab31461031657806327dc297e146103415780632e88ab0b1461041357806338bbfa501461046a5780633f4de62f146105d35780634e69d560146105fe57806360a38a9c1461063757806364a406421461065557806367daa4a31461068057806379b18cd1146106c75780637f6ae770146106f257806382996d9f14610749578063a709c4fe14610774578063adf077911461077e578063b22c36d5146107d5578063bd23eb3914610800578063c61c60fa14610817578063e071956414610821578063f1653f6e1461084c578063ff9b3acf14610877575b34801561016057600080fd5b50610169610907565b005b610173610989565b005b34801561018157600080fd5b5061018a610acb565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156101ca5780820151818401526020810190506101af565b50505050905090810190601f1680156101f75780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b34801561021157600080fd5b5061021a610b6d565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561026857600080fd5b506102956004803603602081101561027f57600080fd5b8101908080359060200190929190505050610b97565b604051808381526020018281526020019250505060405180910390f35b3480156102be57600080fd5b506102c7610bca565b6040518082815260200191505060405180910390f35b3480156102e957600080fd5b506102f2610bd4565b6040518082600281111561030257fe5b60ff16815260200191505060405180910390f35b34801561032257600080fd5b5061032b610be7565b6040518082815260200191505060405180910390f35b34801561034d57600080fd5b506104116004803603604081101561036457600080fd5b81019080803590602001909291908035906020019064010000000081111561038b57600080fd5b82018360208201111561039d57600080fd5b803590602001918460018302840111640100000000831117156103bf57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290505050610bed565b005b34801561041f57600080fd5b50610428610c30565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561047657600080fd5b506105d16004803603606081101561048d57600080fd5b8101908080359060200190929190803590602001906401000000008111156104b457600080fd5b8201836020820111156104c657600080fd5b803590602001918460018302840111640100000000831117156104e857600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019064010000000081111561054b57600080fd5b82018360208201111561055d57600080fd5b8035906020019184600183028401116401000000008311171561057f57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290505050610c56565b005b3480156105df57600080fd5b506105e8610c7a565b6040518082815260200191505060405180910390f35b34801561060a57600080fd5b50610613610c80565b6040518082600281111561062357fe5b60ff16815260200191505060405180910390f35b61063f610c97565b6040518082815260200191505060405180910390f35b34801561066157600080fd5b5061066a610ee6565b6040518082815260200191505060405180910390f35b34801561068c57600080fd5b506106c5600480360360408110156106a357600080fd5b8101908080359060200190929190803515159060200190929190505050610ef0565b005b3480156106d357600080fd5b506106dc610f8c565b6040518082815260200191505060405180910390f35b3480156106fe57600080fd5b50610707610f92565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561075557600080fd5b5061075e610fbc565b6040518082815260200191505060405180910390f35b61077c610fc2565b005b34801561078a57600080fd5b5061079361112f565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b3480156107e157600080fd5b506107ea611155565b6040518082815260200191505060405180910390f35b34801561080c57600080fd5b50610815610907565b005b61081f61115f565b005b34801561082d57600080fd5b5061083661130f565b6040518082815260200191505060405180910390f35b34801561085857600080fd5b50610861611319565b6040518082815260200191505060405180910390f35b34801561088357600080fd5b5061088c61131f565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156108cc5780820151818401526020810190506108b1565b50505050905090810190601f1680156108f95780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b600660019054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc3073ffffffffffffffffffffffffffffffffffffffff16319081150290604051600060405180830381858888f19350505050158015610986573d6000803e3d6000fd5b50565b600660019054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415156109e257fe5b600f60009054906101000a900460ff161515610a6457600760009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc600d549081150290604051600060405180830381858888f19350505050158015610a62573d6000803e3d6000fd5b505b7f1a2c2a2bbbf9d5032486504e1d9485c159203e17fe39ab8eaeea298a97ad3f6860405160405180910390a1600660019054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16ff5b606060088054600181600116156101000203166002900480601f016020809104026020016040519081016040528092919081815260200182805460018160011615610100020316600290048015610b635780601f10610b3857610100808354040283529160200191610b63565b820191906000526020600020905b815481529060010190602001808311610b4657829003601f168201915b5050505050905090565b6000600760009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905090565b600981815481101515610ba657fe5b90600052602060002090600202016000915090508060000154908060010154905082565b6000600b54905090565b600660009054906101000a900460ff1681565b600d5481565b610c2c828260006040519080825280601f01601f191660200182016040528015610c265781602001600182028038833980820191505090505b50610c56565b5050565b600660019054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b60006001026003600080600102815260200190815260200160002081905550505050565b600e5481565b6000600660009054906101000a900460ff16905090565b60003073ffffffffffffffffffffffffffffffffffffffff1631610cef6040805190810160405280600381526020017f55524c00000000000000000000000000000000000000000000000000000000008152506113bd565b1115610dae577f621c2856e3b87f81235f8ac8a22bbb40a0142961960710d00b2b6c380902b57e60405180806020018281038252604a8152602001807f4f7261636c697a6520717565727920776173204e4f542073656e742c20706c6581526020017f6173652061646420736f6d6520455448746f20636f76657220666f722074686581526020017f207175657279206665650000000000000000000000000000000000000000000081525060600191505060405180910390a1610ee2565b7f621c2856e3b87f81235f8ac8a22bbb40a0142961960710d00b2b6c380902b57e6040518080602001828103825260348152602001807f4f7261636c697a65207175657279207761732073656e742c207374616e64696e81526020017f6720627920666f7220746865616e737765722e2e00000000000000000000000081525060400191505060405180910390a1610edb62034bc06040805190810160405280600381526020017f55524c0000000000000000000000000000000000000000000000000000000000815250606060405190810160405280603c81526020017f494e53455254205445524d5320484552452c20706c6561736520726573706f6e81526020017f6420696e74686520666f726d61743a2074727565202f2066616c7365000000008152506117a4565b9050610ee3565b5b90565b6000600d54905090565b610ef8611d5d565b73ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515610f3157600080fd5b7f7472756500000000000000000000000000000000000000000000000000000000610f5a610c97565b1415610f695760019050610f6e565b600090505b80600f60006101000a81548160ff0219169083151502179055505050565b600b5481565b6000600660019054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905090565b600c5481565b600760009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561101b57fe5b6001600281111561102857fe5b600660009054906101000a900460ff16600281111561104357fe5b14151561104f57600080fd5b600e54600c54013414151561106357600080fd5b600660019054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc349081150290604051600060405180830381858888f193505050501580156110cb573d6000803e3d6000fd5b5060096040805190810160405280600160098054905001815260200134815250908060018154018082558091505090600182039060005260206000209060020201600090919290919091506000820151816000015560208201518160010155505050565b600760009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6000600a54905090565b600f60009054906101000a900460ff1615151561117857fe5b600660019054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141580156111fb5750600060028111156111de57fe5b600660009054906101000a900460ff1660028111156111f957fe5b145b80156112085750600d5434145b151561121357600080fd5b33600760006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550600660019054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166108fc349081150290604051600060405180830381858888f193505050501580156112bc573d6000803e3d6000fd5b506001600660006101000a81548160ff021916908360028111156112dc57fe5b02179055507fe289fcb6edad3ac2318541e3a1aadb545e24bfb0dd438445ba6eebae7346676360405160405180910390a1565b6000600c54905090565b600a5481565b60088054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156113b55780601f1061138a576101008083540402835291602001916113b5565b820191906000526020600020905b81548152906001019060200180831161139857829003601f168201915b505050505081565b60008073ffffffffffffffffffffffffffffffffffffffff16600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16148061144557506000611443600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff166120d0565b145b156114565761145460006120db565b505b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166338cc48316040518163ffffffff167c0100000000000000000000000000000000000000000000000000000000028152600401602060405180830381600087803b1580156114dc57600080fd5b505af11580156114f0573d6000803e3d6000fd5b505050506040513d602081101561150657600080fd5b810190808051906020019092919050505073ffffffffffffffffffffffffffffffffffffffff166000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614151561166d57600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166338cc48316040518163ffffffff167c0100000000000000000000000000000000000000000000000000000000028152600401602060405180830381600087803b1580156115f257600080fd5b505af1158015611606573d6000803e3d6000fd5b505050506040513d602081101561161c57600080fd5b81019080805190602001909291905050506000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1663524f3889836040518263ffffffff167c01000000000000000000000000000000000000000000000000000000000281526004018080602001828103825283818151815260200191508051906020019080838360005b838110156117165780820151818401526020810190506116fb565b50505050905090810190601f1680156117435780820380516001836020036101000a031916815260200191505b5092505050602060405180830381600087803b15801561176257600080fd5b505af1158015611776573d6000803e3d6000fd5b505050506040513d602081101561178c57600080fd5b81019080805190602001909291905050509050919050565b60008073ffffffffffffffffffffffffffffffffffffffff16600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16148061182c5750600061182a600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff166120d0565b145b1561183d5761183b60006120db565b505b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166338cc48316040518163ffffffff167c0100000000000000000000000000000000000000000000000000000000028152600401602060405180830381600087803b1580156118c357600080fd5b505af11580156118d7573d6000803e3d6000fd5b505050506040513d60208110156118ed57600080fd5b810190808051906020019092919050505073ffffffffffffffffffffffffffffffffffffffff166000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16141515611a5457600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166338cc48316040518163ffffffff167c0100000000000000000000000000000000000000000000000000000000028152600401602060405180830381600087803b1580156119d957600080fd5b505af11580156119ed573d6000803e3d6000fd5b505050506040513d6020811015611a0357600080fd5b81019080805190602001909291905050506000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1663524f3889856040518263ffffffff167c01000000000000000000000000000000000000000000000000000000000281526004018080602001828103825283818151815260200191508051906020019080838360005b83811015611aff578082015181840152602081019050611ae4565b50505050905090810190601f168015611b2c5780820380516001836020036101000a031916815260200191505b5092505050602060405180830381600087803b158015611b4b57600080fd5b505af1158015611b5f573d6000803e3d6000fd5b505050506040513d6020811015611b7557600080fd5b8101908080519060200190929190505050905062030d403a02670de0b6b3a764000001811115611bac576000600102915050611d56565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1663adf59f99828787876040518563ffffffff167c0100000000000000000000000000000000000000000000000000000000028152600401808481526020018060200180602001838103835285818151815260200191508051906020019080838360005b83811015611c62578082015181840152602081019050611c47565b50505050905090810190601f168015611c8f5780820380516001836020036101000a031916815260200191505b50838103825284818151815260200191508051906020019080838360005b83811015611cc8578082015181840152602081019050611cad565b50505050905090810190601f168015611cf55780820380516001836020036101000a031916815260200191505b50955050505050506020604051808303818588803b158015611d1657600080fd5b505af1158015611d2a573d6000803e3d6000fd5b50505050506040513d6020811015611d4157600080fd5b81019080805190602001909291905050509150505b9392505050565b60008073ffffffffffffffffffffffffffffffffffffffff16600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff161480611de557506000611de3600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff166120d0565b145b15611df657611df460006120db565b505b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166338cc48316040518163ffffffff167c0100000000000000000000000000000000000000000000000000000000028152600401602060405180830381600087803b158015611e7c57600080fd5b505af1158015611e90573d6000803e3d6000fd5b505050506040513d6020811015611ea657600080fd5b810190808051906020019092919050505073ffffffffffffffffffffffffffffffffffffffff166000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614151561200d57600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166338cc48316040518163ffffffff167c0100000000000000000000000000000000000000000000000000000000028152600401602060405180830381600087803b158015611f9257600080fd5b505af1158015611fa6573d6000803e3d6000fd5b505050506040513d6020811015611fbc57600080fd5b81019080805190602001909291905050506000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1663c281d19e6040518163ffffffff167c010000000000000000000000000000000000000000000000000000000002815260040160206040518083038186803b15801561209057600080fd5b505afa1580156120a4573d6000803e3d6000fd5b505050506040513d60208110156120ba57600080fd5b8101908080519060200190929190505050905090565b6000813b9050919050565b60006120e56120ec565b9050919050565b60008061210c731d3b2638a7cc9f2cb3d298a3da7a90b67e5506ed6120d0565b11156121ae57731d3b2638a7cc9f2cb3d298a3da7a90b67e5506ed600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506121a56040805190810160405280600b81526020017f6574685f6d61696e6e6574000000000000000000000000000000000000000000815250612643565b60019050612640565b60006121cd73c03a2615d5efaf5f49f60b7bb6583eaec212fdf16120d0565b111561226f5773c03a2615d5efaf5f49f60b7bb6583eaec212fdf1600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506122666040805190810160405280600c81526020017f6574685f726f707374656e330000000000000000000000000000000000000000815250612643565b60019050612640565b600061228e73b7a07bcf2ba2f2703b24c0691b5278999c59ac7e6120d0565b11156123305773b7a07bcf2ba2f2703b24c0691b5278999c59ac7e600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506123276040805190810160405280600981526020017f6574685f6b6f76616e0000000000000000000000000000000000000000000000815250612643565b60019050612640565b600061234f73146500cfd35b22e4a392fe0adc06de1a1368ed486120d0565b11156123f15773146500cfd35b22e4a392fe0adc06de1a1368ed48600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506123e86040805190810160405280600b81526020017f6574685f72696e6b656279000000000000000000000000000000000000000000815250612643565b60019050612640565b600061241073a2998efd205fb9d4b4963afb70778d6354ad3a416120d0565b11156124b25773a2998efd205fb9d4b4963afb70778d6354ad3a41600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506124a96040805190810160405280600a81526020017f6574685f676f65726c6900000000000000000000000000000000000000000000815250612643565b60019050612640565b60006124d1736f485c8bf6fc43ea212e93bbf8ce046c7f1cb4756120d0565b111561253557736f485c8bf6fc43ea212e93bbf8ce046c7f1cb475600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060019050612640565b60006125547320e12a1f859b3feae5fb2a0a32c18f5a65555bbf6120d0565b11156125b8577320e12a1f859b3feae5fb2a0a32c18f5a65555bbf600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060019050612640565b60006125d77351efaf4c8b3c9afbd5ab9f4bbc82784ab6ef8faa6120d0565b111561263b577351efaf4c8b3c9afbd5ab9f4bbc82784ab6ef8faa600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060019050612640565b600090505b90565b806002908051906020019061265992919061265d565b5050565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061269e57805160ff19168380011785556126cc565b828001600101855582156126cc579182015b828111156126cb5782518255916020019190600101906126b0565b5b5090506126d991906126dd565b5090565b6126ff91905b808211156126fb5760008160009055506001016126e3565b5090565b9056fea165627a7a72305820b8827ad9130ef8dd3fc3376e015ea2c1c129ee9e0894ade00909c701de21ed870029'


            private_key = form.cleaned_data['private_key']
            RentalAgreement = web3.eth.contract(abi=abi, bytecode=bytecode)

            acct = web3.eth.account.privateKeyToAccount(private_key)

            rentPrice = object.price
            rentLength = form.cleaned_data['rentLength']
            rentHouse = object.title

            tx_build = RentalAgreement.constructor(rentPrice, rentHouse, rentLength).buildTransaction(
                {'from': acct.address,
                 'nonce': web3.eth.getTransactionCount(acct.address), })

            signed = acct.signTransaction(tx_build)

            tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)

            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

            print(tx_receipt.contractAddress)

            newContract = Contract.objects.create()
            newContract.sc_address = tx_receipt.contractAddress
            newContract.term = rentLength
            newContract.paidsCount = rentLength
            newContract.save()

            object.contract = newContract
            object.is_published = True
            object.save()

            return redirect('dashboard')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DeployingForm()

    return render(request, 'listings/deploying.html', {'form': form})




def listing_on_dashboard(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    sc_address = listing.contract.sc_address

    kovan_url = 'https://kovan.infura.io/v3/050656a9183d4fd7bcac660f237a1724'
    web3 = Web3(Web3.HTTPProvider(kovan_url))
    web3.eth.defaultAccount = Web3.toChecksumAddress(request.user.eth_acc)

    print(web3.eth.defaultAccount   )

    abi = json.loads(
        '[{"constant":false,"inputs":[],"name":"TerminateContract","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getHouse","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTenant","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"rentsPaid","outputs":[{"name":"month","type":"uint256"},{"name":"amount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTermLength","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"status","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"securityDeposit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_myid","type":"bytes32"},{"name":"_result","type":"string"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"renter","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_myid","type":"bytes32"},{"name":"_result","type":"string"},{"name":"_proof","type":"bytes"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"lateFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getStatus","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"CheckTerms","outputs":[{"name":"","type":"bytes32"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getSecurityDeposit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"myid","type":"bytes32"},{"name":"result","type":"bool"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"termLength","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getRenter","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"rent","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"payRent","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"tenant","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTimeCreated","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"tokenFallback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"beginLease","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getRent","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"timeCreated","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"house","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_rent","type":"uint256"},{"name":"_house","type":"string"},{"name":"_termLength","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":false,"stateMutability":"nonpayable","type":"fallback"},{"anonymous":false,"inputs":[],"name":"rentPaid","type":"event"},{"anonymous":false,"inputs":[],"name":"contractActive","type":"event"},{"anonymous":false,"inputs":[],"name":"contractTerminated","type":"event"},{"anonymous":false,"inputs":[],"name":"termBreached","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"description","type":"string"}],"name":"LogNewOraclizeQuery","type":"event"}]')

    address = Web3.toChecksumAddress(sc_address)

    contract = web3.eth.contract(
        address=address,
        abi=abi
    )

    print(sc_address)

    listing.contract.status = contract.functions.getStatus().call()
    listing.contract.tenant = contract.functions.getTenant().call()
    listing.contract.save()


    try:
         Contact.objects.get(contract=listing.contract)
    except ObjectDoesNotExist:
        isTenantHere = 'Пока никто не заключил контракт'

    else:
        tenant = Contact.objects.get(contract=listing.contract)
        isTenantHere = tenant.user

    print(isTenantHere)
    context = {

        'listing':listing,
        'tenant': isTenantHere

    }
    return render(request, 'listings/listing_dashboard.html', context)



def get_user_actions(request, listing):
    listing = Listing.objects.get(id=listing)
    count = listing.contract.term - listing.contract.paidsCount
    context = {
        'listing': listing,
        'count': count,
    }
    return render(request, 'listings/user_actions.html', context)


def pay_mail(listing_id, contact_id):
    list = Listing.objects.get(id=listing_id)
    new_contact = Contact.objects.get(id=contact_id)
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    now = datetime.datetime.now()
    subject = 'Совершена оплата по вашей квартире' + ': ' + str(list.title)
    message = 'Здравствуйте,' + '\n\n' + 'оплачена арендная плата за' + ' ' + str(now.strftime("%B"))  + '\n\n' + 'Адрес хэша полученного в итоге оплаты:' + ' ' + 'https://kovan.etherscan.io/tx/' + str(
        list.contract.last_pay_tr) + '\n\n' + 'Почта арендующего: '  + str(
        new_contact.user.email) + '\n' + 'Для более точной информации зайдите в ваш профиль https://cryptrent24.com/dashboard' + '\n\n' + 'С уважением,' + '\n' + 'команда CryptRent' + '\n\n'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [list.user.email, ]
    send_mail(subject, message, email_from, recipient_list)
    return print('Email about new contact')


def get_pay(request, listing):
    # if this is a POST request we need to process the form data
    print('hello')

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PayForm(request.POST)
        # check whether it's valid:

        if form.is_valid():


            property = Listing.objects.get(id=listing)
            kovan_url = 'https://kovan.infura.io/v3/050656a9183d4fd7bcac660f237a1724'
            web3 = Web3(Web3.HTTPProvider(kovan_url))
            web3.eth.defaultAccount = Web3.toChecksumAddress(request.user.eth_acc)

            abi = json.loads('[{"constant":false,"inputs":[],"name":"TerminateContract","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getHouse","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTenant","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"rentsPaid","outputs":[{"name":"month","type":"uint256"},{"name":"amount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTermLength","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"status","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"securityDeposit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_myid","type":"bytes32"},{"name":"_result","type":"string"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"renter","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_myid","type":"bytes32"},{"name":"_result","type":"string"},{"name":"_proof","type":"bytes"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"lateFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getStatus","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"CheckTerms","outputs":[{"name":"","type":"bytes32"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getSecurityDeposit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"myid","type":"bytes32"},{"name":"result","type":"bool"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"termLength","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getRenter","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"rent","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"payRent","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"tenant","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTimeCreated","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"tokenFallback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"beginLease","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getRent","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"timeCreated","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"house","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_rent","type":"uint256"},{"name":"_house","type":"string"},{"name":"_termLength","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":false,"stateMutability":"nonpayable","type":"fallback"},{"anonymous":false,"inputs":[],"name":"rentPaid","type":"event"},{"anonymous":false,"inputs":[],"name":"contractActive","type":"event"},{"anonymous":false,"inputs":[],"name":"contractTerminated","type":"event"},{"anonymous":false,"inputs":[],"name":"termBreached","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"description","type":"string"}],"name":"LogNewOraclizeQuery","type":"event"}]')

            private_key = form.cleaned_data['private_key']

            acct = web3.eth.account.privateKeyToAccount(private_key)

            address = Web3.toChecksumAddress(property.contract.sc_address)

            contract = web3.eth.contract(
                address=address,
                abi=abi
            )

            price = property.price

            tx_hash = contract.functions.payRent().buildTransaction(
                {'from': acct.address, 'value': web3.toWei(price, 'wei'),
                 'nonce': web3.eth.getTransactionCount(acct.address), })

            signed = acct.signTransaction(tx_hash)

            tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)

            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)



            print(tx_receipt)

            property.contract.last_pay_tr = tx_receipt.transactionHash.hex()
            if property.contract.paidsCount is None:
                property.contract.paidsCount= property.contract.term -1
            else:
                property.contract.paidsCount = property.contract.paidsCount - 1

            property.contract.status = contract.functions.getStatus().call()

            property.contract.save()

            contact = Contact.objects.get(contract=property.contract)

            pay_mail(property.id, contact.id )


            return redirect(get_user_actions, listing=listing)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PayForm()

    return redirect(get_user_actions, listing=listing)


def get_terminated(request, listing):
    # if this is a POST request we need to process the form data
    print('hello')

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TerminationForm(request.POST)
        # check whether it's valid:

        if form.is_valid():


            property = Listing.objects.get(id=listing)
            kovan_url = 'https://kovan.infura.io/v3/050656a9183d4fd7bcac660f237a1724'
            web3 = Web3(Web3.HTTPProvider(kovan_url))
            web3.eth.defaultAccount = Web3.toChecksumAddress(request.user.eth_acc)

            abi = json.loads('[{"constant":false,"inputs":[],"name":"TerminateContract","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getHouse","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTenant","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"rentsPaid","outputs":[{"name":"month","type":"uint256"},{"name":"amount","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTermLength","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"status","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"securityDeposit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_myid","type":"bytes32"},{"name":"_result","type":"string"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"renter","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_myid","type":"bytes32"},{"name":"_result","type":"string"},{"name":"_proof","type":"bytes"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"lateFee","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getStatus","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"CheckTerms","outputs":[{"name":"","type":"bytes32"}],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getSecurityDeposit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"myid","type":"bytes32"},{"name":"result","type":"bool"}],"name":"__callback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"termLength","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getRenter","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"rent","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"payRent","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"tenant","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getTimeCreated","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"tokenFallback","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"beginLease","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[],"name":"getRent","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"timeCreated","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"house","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_rent","type":"uint256"},{"name":"_house","type":"string"},{"name":"_termLength","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":false,"stateMutability":"nonpayable","type":"fallback"},{"anonymous":false,"inputs":[],"name":"rentPaid","type":"event"},{"anonymous":false,"inputs":[],"name":"contractActive","type":"event"},{"anonymous":false,"inputs":[],"name":"contractTerminated","type":"event"},{"anonymous":false,"inputs":[],"name":"termBreached","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"description","type":"string"}],"name":"LogNewOraclizeQuery","type":"event"}]')

            private_key = form.cleaned_data['private_key']

            acct = web3.eth.account.privateKeyToAccount(private_key)

            address = Web3.toChecksumAddress(property.contract.sc_address)

            contract = web3.eth.contract(
                address=address,
                abi=abi
            )


            tx_hash = contract.functions.TerminateContract().buildTransaction(
                {'from': acct.address,
                 'nonce': web3.eth.getTransactionCount(acct.address), 'value': web3.toWei(1000000, 'wei') })

            signed = acct.signTransaction(tx_hash)

            tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)

            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)



            print(property.contract_id)
            cont_on_delete = Contract.objects.get(id=property.contract_id)

            try:
                Contact.objects.get(contract=cont_on_delete)
            except ObjectDoesNotExist:
                print('Пользователь не заключал контракт')
            else:
                change_message_object = Contact.objects.get(contract=cont_on_delete)
                change_message_object.message = 'Ваш контракт закрыт. Свяжитесь с арендатором ' + ' ' + '+7913000000'
                change_message_object.save()

            cont_on_delete.delete()

            property.contract = None
            property.is_published = False
            property.save()



            return redirect('dashboard')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TerminationForm()

    return redirect('dashboard')



