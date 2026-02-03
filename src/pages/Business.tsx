import { useState } from "react";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import {
  Building2,
  MapPin,
  Phone,
  Mail,
  Globe,
  Calendar,
  Users,
  IndianRupee,
  Edit2,
  Save,
  Plus,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const industries = [
  "Manufacturing",
  "Retail",
  "Services",
  "Agriculture",
  "Logistics",
  "E-commerce",
  "Healthcare",
  "Construction",
  "Food & Beverage",
  "Technology",
];

const businessTypes = [
  "Sole Proprietorship",
  "Partnership",
  "LLP",
  "Private Limited",
  "Public Limited",
  "One Person Company",
];

export default function Business() {
  const { toast } = useToast();
  const [isEditing, setIsEditing] = useState(false);
  const [businessData, setBusinessData] = useState({
    name: "TechCraft Solutions Pvt. Ltd.",
    industry: "technology",
    type: "Private Limited",
    gstin: "27AABCU9603R1ZM",
    pan: "AABCU9603R",
    cin: "U74999MH2018PTC123456",
    address: "123, Business Park, Andheri East, Mumbai, Maharashtra - 400069",
    phone: "+91 22 4567 8900",
    email: "info@techcraft.co.in",
    website: "www.techcraft.co.in",
    established: "2018",
    employees: "25-50",
    annualRevenue: "₹1-5 Cr",
    description: "TechCraft Solutions is a technology consulting firm specializing in digital transformation for SMEs.",
  });

  const handleSave = () => {
    setIsEditing(false);
    toast({
      title: "Profile updated",
      description: "Your business profile has been saved successfully.",
    });
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Business Profile</h1>
            <p className="text-muted-foreground">
              Manage your business information and settings
            </p>
          </div>
          {isEditing ? (
            <Button onClick={handleSave} className="gap-2">
              <Save className="h-4 w-4" />
              Save Changes
            </Button>
          ) : (
            <Button variant="outline" onClick={() => setIsEditing(true)} className="gap-2">
              <Edit2 className="h-4 w-4" />
              Edit Profile
            </Button>
          )}
        </div>

        {/* Business Overview Card */}
        <Card className="card-elevated">
          <CardContent className="p-6">
            <div className="flex items-start gap-6">
              <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground">
                <Building2 className="h-10 w-10" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-3">
                  <h2 className="text-2xl font-bold">{businessData.name}</h2>
                  <Badge className="bg-success/10 text-success">Active</Badge>
                </div>
                <p className="mt-1 text-muted-foreground">{businessData.description}</p>
                <div className="mt-4 flex flex-wrap gap-4 text-sm">
                  <div className="flex items-center gap-1 text-muted-foreground">
                    <MapPin className="h-4 w-4" />
                    Mumbai, Maharashtra
                  </div>
                  <div className="flex items-center gap-1 text-muted-foreground">
                    <Users className="h-4 w-4" />
                    {businessData.employees} employees
                  </div>
                  <div className="flex items-center gap-1 text-muted-foreground">
                    <Calendar className="h-4 w-4" />
                    Est. {businessData.established}
                  </div>
                  <div className="flex items-center gap-1 text-muted-foreground">
                    <IndianRupee className="h-4 w-4" />
                    {businessData.annualRevenue} revenue
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Basic Information */}
          <Card className="card-elevated">
            <CardHeader>
              <CardTitle>Basic Information</CardTitle>
              <CardDescription>Primary business details and registration info</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Business Name</Label>
                <Input
                  value={businessData.name}
                  onChange={(e) => setBusinessData({ ...businessData, name: e.target.value })}
                  disabled={!isEditing}
                />
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label>Industry</Label>
                  <Select
                    value={businessData.industry}
                    onValueChange={(value) => setBusinessData({ ...businessData, industry: value })}
                    disabled={!isEditing}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {industries.map((ind) => (
                        <SelectItem key={ind} value={ind.toLowerCase()}>
                          {ind}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label>Business Type</Label>
                  <Select
                    value={businessData.type}
                    onValueChange={(value) => setBusinessData({ ...businessData, type: value })}
                    disabled={!isEditing}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {businessTypes.map((type) => (
                        <SelectItem key={type} value={type}>
                          {type}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div className="space-y-2">
                <Label>Description</Label>
                <Textarea
                  value={businessData.description}
                  onChange={(e) => setBusinessData({ ...businessData, description: e.target.value })}
                  disabled={!isEditing}
                  rows={3}
                />
              </div>
            </CardContent>
          </Card>

          {/* Registration Details */}
          <Card className="card-elevated">
            <CardHeader>
              <CardTitle>Registration Details</CardTitle>
              <CardDescription>Tax and legal registration information</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>GSTIN</Label>
                <Input
                  value={businessData.gstin}
                  onChange={(e) => setBusinessData({ ...businessData, gstin: e.target.value })}
                  disabled={!isEditing}
                  className="font-mono"
                />
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label>PAN</Label>
                  <Input
                    value={businessData.pan}
                    onChange={(e) => setBusinessData({ ...businessData, pan: e.target.value })}
                    disabled={!isEditing}
                    className="font-mono"
                  />
                </div>
                <div className="space-y-2">
                  <Label>CIN</Label>
                  <Input
                    value={businessData.cin}
                    onChange={(e) => setBusinessData({ ...businessData, cin: e.target.value })}
                    disabled={!isEditing}
                    className="font-mono"
                  />
                </div>
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="space-y-2">
                  <Label>Employees</Label>
                  <Select
                    value={businessData.employees}
                    onValueChange={(value) => setBusinessData({ ...businessData, employees: value })}
                    disabled={!isEditing}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="1-10">1-10</SelectItem>
                      <SelectItem value="11-25">11-25</SelectItem>
                      <SelectItem value="25-50">25-50</SelectItem>
                      <SelectItem value="50-100">50-100</SelectItem>
                      <SelectItem value="100+">100+</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label>Established</Label>
                  <Input
                    value={businessData.established}
                    onChange={(e) => setBusinessData({ ...businessData, established: e.target.value })}
                    disabled={!isEditing}
                  />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Contact Information */}
          <Card className="card-elevated lg:col-span-2">
            <CardHeader>
              <CardTitle>Contact Information</CardTitle>
              <CardDescription>Business contact details and address</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label>Address</Label>
                    <Textarea
                      value={businessData.address}
                      onChange={(e) => setBusinessData({ ...businessData, address: e.target.value })}
                      disabled={!isEditing}
                      rows={2}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>Phone</Label>
                    <div className="relative">
                      <Phone className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                      <Input
                        value={businessData.phone}
                        onChange={(e) => setBusinessData({ ...businessData, phone: e.target.value })}
                        disabled={!isEditing}
                        className="pl-10"
                      />
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label>Email</Label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                      <Input
                        value={businessData.email}
                        onChange={(e) => setBusinessData({ ...businessData, email: e.target.value })}
                        disabled={!isEditing}
                        className="pl-10"
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label>Website</Label>
                    <div className="relative">
                      <Globe className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                      <Input
                        value={businessData.website}
                        onChange={(e) => setBusinessData({ ...businessData, website: e.target.value })}
                        disabled={!isEditing}
                        className="pl-10"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Add Another Business */}
        <Card className="card-elevated border-dashed">
          <CardContent className="flex flex-col items-center justify-center p-8">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-muted">
              <Plus className="h-6 w-6 text-muted-foreground" />
            </div>
            <p className="mt-4 font-medium">Add Another Business</p>
            <p className="mt-1 text-sm text-muted-foreground">
              Manage multiple businesses from a single dashboard
            </p>
            <Button variant="outline" className="mt-4">
              Add Business
            </Button>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
