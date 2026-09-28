import numpy as np
import os; currentDir = os.getcwd()
from datetime import datetime
import matplotlib; matplotlib.use('QtAgg')
from matplotlib.ticker import Locator; Locator.MAXTICKS = 1_500
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import AutoMinorLocator

class loan():
    def __init__(self, principal, transfer_fee, null_apr_term, apr, monthly_payment=0.0):
        self.principal = principal #in $
        self.transfer_fee = transfer_fee #in %
        self.starting_principle = self.principal*(1+self.transfer_fee/100)
        self.null_apr_term = null_apr_term #in mo

        self.apr = apr #in %
        self.mpr = self.apr/12
        self.dpr = self.apr/365
        self.monthly_payment = monthly_payment
        
        self.ledger = [{}]
        i = 0
        self.ledger[i]["month"] = i
        self.ledger[i]["start"] = self.starting_principle
        self.ledger[i]["interest"] = ( self.ledger[i]["start"]*(self.mpr/100) ) * (i>self.null_apr_term)
        self.ledger[i]["payment"] = self.monthly_payment
        self.ledger[i]["final"] = (self.ledger[i]["start"]+self.ledger[i]["interest"])-self.ledger[i]["payment"]



    def run(self):
        try:
            i=1; w=0
            while (self.ledger[i-1]["final"]>0): 
                self.ledger.append({})
                self.ledger[i]["month"] = i
                self.ledger[i]["start"] = self.ledger[i-1]["final"]
                self.ledger[i]["interest"] = ( self.ledger[i]["start"]*(self.mpr/100) ) * (i>self.null_apr_term)
                self.ledger[i]["payment"] = self.monthly_payment
                self.ledger[i]["final"] = (self.ledger[i]["start"]+self.ledger[i]["interest"])-self.ledger[i]["payment"]
                if (self.ledger[i]["interest"]>self.ledger[i]["payment"]):
                    print(f"WARNING: Intresest not paid for month {i}! {w}/24 warnings")
                    w+=1
                if (self.ledger[i]["final"] > self.ledger[0]["start"]):
                    print(
                        "FATAL: Runaway Debt " + "due to low dynamic payments! "*(self.ledger[i]["final"] > self.ledger[0]["start"]) + "Due to 2 years (total) missed interest payments! "*(w>24)
                    )
                    break
                    #quit(code=None)
                i+=1
        finally:
            self.loan_duration = i/12 #in years



    def show(self, withText:bool=True):
        print(
            f"""
            principal: {self.principal}
            transaction fee: {self.transfer_fee}
            starting principal: {self.starting_principle} 
            null apr term: {self.null_apr_term}
    
            apr: {self.apr} 
            mpr: {self.mpr}
            dpr: {self.dpr}
        
            ledger: {str(self.ledger).replace("[","\n").replace("},","},\n").replace("{'","\t\t{")}
            
            loan duration: {self.loan_duration} 
            """*withText
        )
        
        ###_deserializer_###
        ax1, ax2, ax3, ax4, ax5 = [], [], [], [], []
        for block in self.ledger:
            month, start, interest, payment, final = block.values()
            ax1.append(month)
            ax2.append(start)
            ax3.append(interest)
            ax4.append(payment)
            ax5.append(final)
        ###_###

        fig, graph = plt.subplots()
        fig.subplots_adjust(
            top=0.962, bottom=0.065, left=0.059, right=0.9, hspace=0.2, wspace=0.2
            )
        graph.plot(ax1, ax2, label="start")
        graph.plot(ax1, ax3, label="interest")
        graph.plot(ax1, ax4, label="payment")
        graph.plot(ax1, ax5, label="final")
        graph.set_title(label="loan information", loc="center", pad=1)
        
        graph.set_ylabel(ylabel="Amount ($)", loc="center")
        graph.yaxis.grid(visible=True, which="major")
        graph.yaxis.grid(visible=False, which="minor")#
        graph.yaxis.set_minor_locator(AutoMinorLocator())
        graph.yaxis.set_major_locator(ticker.MultipleLocator(500))

        graph.set_xlabel(xlabel="Time (mo)", loc="center")
        graph.xaxis.grid(visible=True, which="major")
        graph.xaxis.grid(visible=False, which="minor")
        graph.xaxis.set_minor_locator(AutoMinorLocator())
        #graph.xaxis.set_major_locator(ticker.MultipleLocator(1))
        
        plt.xticks(rotation=45)
        graph.legend()
        # Safely maximize the window regardless of the operating system
        backend = plt.get_current_fig_manager()
        try:
            backend.window.state('zoomed')  # Works on Windows
        except AttributeError:
            try:
                backend.resize(*backend.window.maxsize())  # Works on Linux / Mac
            except AttributeError:
                backend.full_screen_toggle()  # Fallback
        fig.savefig(f"{currentDir}/Figure - {datetime.now().strftime('%Y-%m-%d at %H-%M-%S')}.svg", format="svg", pad_inches=0.1)
        plt.show()
    ###
###
       
    
LOAN = loan(principal= , transfer_fee=, null_apr_term=, apr=, monthly_payment= )
LOAN.run()
LOAN.show(withText=True)

