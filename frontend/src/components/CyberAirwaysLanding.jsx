import React, { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { useToast } from "../hooks/use-toast";
import { Toaster } from "./ui/toaster";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CyberAirwaysLanding = () => {
  const [bookingRef, setBookingRef] = useState("");
  const [lastName, setLastName] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleFlightReadinessCheck = async () => {
    if (!bookingRef.trim() || !lastName.trim()) {
      toast({
        title: "Error",
        description: "Please fill in both Booking Reference and Last Name",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    try {
      const response = await axios.post(`${API}/flight-readiness`, {
        bookingReference: bookingRef,
        lastName: lastName,
      });
      
      toast({
        title: "Flight Readiness Check",
        description: `Status: ${response.data.status} - ${response.data.message}`,
      });
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to check flight readiness. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="w-full bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="text-2xl font-bold text-[#002147]">
            CyberAirways
          </div>
          <div className="flex items-center gap-8">
            <nav className="flex items-center gap-6">
              <a href="#" className="text-[#002147] hover:text-[#C0C0C0] transition-colors">
                Book
              </a>
              <a href="#" className="text-[#002147] hover:text-[#C0C0C0] transition-colors">
                Manage
              </a>
              <a href="#" className="text-[#002147] hover:text-[#C0C0C0] transition-colors">
                Help
              </a>
            </nav>
            <Button className="bg-[#002147] hover:bg-[#001a38] text-white">
              Log in
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content / Hero Section */}
      <main 
        className="relative min-h-[80vh] flex items-center justify-center bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url('https://images.unsplash.com/photo-1575427862440-9afbff3e64ac')`
        }}
      >
        <Card className="w-full max-w-md mx-4 bg-white/95 backdrop-blur-sm shadow-2xl">
          <CardHeader className="text-center pb-6">
            <CardTitle className="text-3xl font-bold text-[#002147] mb-2">
              Manage Your Booking
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="check-in" className="w-full">
              <TabsList className="grid w-full grid-cols-2 mb-6">
                <TabsTrigger 
                  value="check-in" 
                  className="data-[state=active]:bg-[#002147] data-[state=active]:text-white"
                >
                  Check-in / Flight status
                </TabsTrigger>
                <TabsTrigger 
                  value="change" 
                  className="data-[state=active]:bg-[#002147] data-[state=active]:text-white"
                >
                  Change booking
                </TabsTrigger>
              </TabsList>
              
              <TabsContent value="check-in" className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="booking-ref" className="text-[#002147] font-medium">
                    Booking Reference
                  </Label>
                  <Input
                    id="booking-ref"
                    type="text"
                    placeholder="Enter booking reference"
                    value={bookingRef}
                    onChange={(e) => setBookingRef(e.target.value)}
                    className="border-gray-300 focus:border-[#002147] focus:ring-[#002147]"
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="last-name" className="text-[#002147] font-medium">
                    Last Name
                  </Label>
                  <Input
                    id="last-name"
                    type="text"
                    placeholder="Enter last name"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    className="border-gray-300 focus:border-[#002147] focus:ring-[#002147]"
                  />
                </div>
                
                <Button 
                  onClick={handleFlightReadinessCheck}
                  disabled={isLoading}
                  className="w-full bg-[#002147] hover:bg-[#001a38] text-white py-3 text-lg font-semibold mt-6"
                >
                  {isLoading ? "Checking..." : "Check Flight Readiness"}
                </Button>
              </TabsContent>
              
              <TabsContent value="change" className="space-y-4">
                <div className="text-center py-8 text-gray-600">
                  <p>Change booking functionality coming soon.</p>
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </main>

      {/* Footer */}
      <footer className="w-full bg-gray-800 text-white py-12">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-4 gap-8">
            <div>
              <h3 className="font-semibold mb-4">About CA</h3>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors">Our Story</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Leadership</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Sustainability</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Careers</h3>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors">Current Openings</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Graduate Programs</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Benefits</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Contact Us</h3>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors">Customer Service</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Feedback</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Lost & Found</a></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-4">Legal</h3>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms & Conditions</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Cookie Policy</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 CyberAirways. All rights reserved.</p>
          </div>
        </div>
      </footer>
      
      <Toaster />
    </div>
  );
};

export default CyberAirwaysLanding;